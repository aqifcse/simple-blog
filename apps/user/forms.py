from urllib import request
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from apps.user.models import User, NewsReader
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation

class UserRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_user = True
        user.save()
        news_reader = NewsReader.objects.create(user=user)
        return user


class UserLoginForm(AuthenticationForm):
    user_type = forms.CharField(max_length=150)

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'invalid': _("Invalid user input!"),
        'inactive': _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user_type = self.cleaned_data.get('user_type')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                if self.user_cache.is_admin and user_type == 'admin':
                    self.confirm_login_allowed(self.user_cache)
                elif self.user_cache.is_user and user_type == 'user':
                    self.confirm_login_allowed(self.user_cache)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid'],
                        code='invalid',
                    )

        return self.cleaned_data

class EmailValidationOnForgotPassword(PasswordResetForm):

    error_messages = {
        'unregistered': _("The email is not registered. Please register"),
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(self.error_messages['unregistered'], code='unregistered',)

        return email