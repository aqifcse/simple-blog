from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from apps.user.decorators import user_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import News, Category

# Create your views here.

class HomeView(ListView):
    template_name = 'home/home.html'
    context_object_name = 'news_details'

    def get_queryset(self):
        queryset = {
            # "categories": Category.objects.all(),
            "newss": News.objects.all()
        }
        print(queryset)
        return queryset

@method_decorator([login_required, user_required], name='dispatch')
class UserHomeView(TemplateView):
    template_name = 'home/user_home.html'
    context_object_name = 'news_details'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        pass


class Contact(TemplateView):
    template_name = 'home/contact.html'
    context_object_name = 'apps'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        pass

class About(TemplateView):
    template_name = 'home/about.html'
    context_object_name = 'apps'

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        pass