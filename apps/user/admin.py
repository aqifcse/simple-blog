from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User, NewsReader

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserModelAdmin(UserAdmin):
    model = User
    list_display = ('email', 'is_admin', 'is_user', 'is_active', 'email_confirmed')
    list_filter = ('email', 'is_admin', 'is_user','is_active', 'email_confirmed')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_user','is_active', 'email_confirmed')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)



# Register your models here.
admin.site.unregister(Group)
admin.site.register(User, UserModelAdmin)
admin.site.register(NewsReader)
