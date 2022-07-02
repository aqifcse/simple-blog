from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.shortcuts import redirect, render
from apps.user.models import User
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, PasswordResetView
from django.utils.http import url_has_allowed_host_and_scheme
from apps.user.forms import UserLoginForm, UserRegistrationForm
from .decorators import admin_required, user_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from apps.home.models import Category, News
from django.db.models import Q

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings

from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, TemplateView, View
from django.utils.encoding import force_str
from django.contrib.auth import login
from rest_framework.generics import DestroyAPIView


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'email'

# Create your views here.
class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {
            'form': form,
            'user_type': 'user',
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            # current_site = get_current_site(request)
            # subject = 'Activate Your User account'
            # message = render_to_string('users/account_activation_email.html', {
            #     'user': user,
            #     'domain': current_site.domain,
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': account_activation_token.make_token(user),
            # })
            # user.email_user(subject, message, 'aqif.cse@gmail.com')

            # email_sent_message = 'An email has been sent to ' + str(user.email) + ' Please check your email and click on the confirmation link to confirm your account'

            return render(request, 'users/login.html', {
                'success_message': email_sent_message,
            })

        return render(request, self.template_name, {'form': form})

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            #print(uid)
            user = User.objects.get(pk=uid)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            #print("Does not exists")
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            if user.is_user:
                user.is_active = True
            elif user.is_developer:
                user.is_active = False

            user.email_confirmed = True
            user.save()
            login(request, user)

            if user.is_user:
                user_success_account_message = email_sent_message = 'Hi!! ' + str(user.username) + ' Your account have been confirmed. Please log with your given username and password.'

                return render(request, 'users/login.html', {
                    'success_message': user_success_account_message,
                })
            elif user.is_developer:
                admin_approval_message = 'Hi ' + str(user.username) +'!! Please wait for the activation status email from the admin. Once you get it, you will be able to login with your given username and password.  '
                return render(request, 'users/login.html', {
                    'success_message': admin_approval_message,
                })            
        else:
            return render(request, 'users/login.html', {
                'error_message': 'The confirmation link was invalid, possibly because it has already been used.'
            })


class UserLoginView(LoginView):
    form_class = UserLoginForm

    def get_success_url(self):
        
        if self.request.user.is_admin:
            return reverse_lazy('user:portal-admin')
        elif self.request.user.is_user:
            return reverse_lazy('home:user-home')
        else:
            return reverse_lazy('home:user-home')

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''


@method_decorator([login_required, admin_required], name='dispatch')
class DashboardAdminView(ListView):
    model = User
    template_name = 'users/admin_portal.html'
    # context_object_name = 'apps'
    # ordering = ['date']

    def get_queryset(self):
        # total_download = App.objects.aggregate(Sum('downloads'))

        # #year_list = list(range(1990, 2041, 1))

        # queryset = {
        #     "total_upload" : App.objects.filter(is_active = True),
        #     "total_download": total_download['downloads__sum'],
        #     #"year_list": year_list
        # }
        # return queryset
        pass

@method_decorator([login_required, admin_required], name='dispatch')
class AdminUserList(ListView):
    model = User
    template_name = 'users/admin_user_list.html'
    context_object_name = 'user_obj'
    paginate_by = 10

    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return User.objects.filter(
                Q(user__username__icontains=form) | 
                Q(user__email__icontains=form) | 
                Q(user__first_name__icontains=form) | 
                Q(user__last_name__icontains=form)
            ).order_by('id')
        queryset = User.objects.all().order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class AdminCategoryList(ListView):
    model = Category
    template_name = 'users/admin_category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return Category.objects.filter(
                Q(__icontains=form) | 
                Q(app_version_code__icontains=form) |
                Q(app_version_name__icontains=form) |
                Q(app_package_name__icontains=form) | 
                Q(app_short_description__icontains=form)
            ).order_by('id').reverse()
        queryset = Category.objects.all().order_by('id').reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class AdminNewsList(ListView):
    model = News
    template_name = 'users/admin_news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return News.objects.filter(
                Q(app__app_name__icontains=form) | 
                Q(app_version_code__icontains=form) |
                Q(app_version_name__icontains=form) |
                Q(app_package_name__icontains=form) | 
                Q(app_short_description__icontains=form)
            ).order_by('id').reverse()
        queryset = News.objects.all().order_by('id').reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class AdminNewsByCategoryList(ListView):
    model = News
    template_name = 'users/admin_news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        form = self.request.GET.get('q')
        if form:
            return News.objects.filter(
                Q(app__app_name__icontains=form) | 
                Q(app_version_code__icontains=form) |
                Q(app_version_name__icontains=form) |
                Q(app_package_name__icontains=form) | 
                Q(app_short_description__icontains=form)
            ).order_by('id').reverse()
        category_slug = self.kwargs['category_slug']
        print(category_slug)
        queryset = News.objects.filter(category__category_slug=category_slug).order_by('id').reverse()
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['q'] = self.request.GET.get('q')
        return super().get_context_data(**kwargs)

@method_decorator([login_required, admin_required], name='dispatch')
class AdminCategoryAdd(CreateView):
    model 			= Category
    fields 			= ['category_name', 'category_slug']
    template_name 	= 'users/admin_category_add.html'
    success_url		= reverse_lazy('user:admin-category-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        super(AdminCategoryAdd, self).form_valid(form)
        return redirect('user:admin-category-list')

@method_decorator([login_required, admin_required], name='dispatch')
class AdminNewsAdd(CreateView):
    model 			= News
    fields 			= ['news_slug', 'title', 'image', 'description', 'reported_by', 'category']
    template_name 	= 'users/admin_news_add.html'
    success_url		= reverse_lazy('user:admin-news-list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.reported_at = datetime.now()
        super(AdminNewsAdd, self).form_valid(form)
        return redirect('user:admin-news-list')
