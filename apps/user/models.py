from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomUserManager

from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class NewsReader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_active = models.BooleanField(default=False)