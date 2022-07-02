from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

#from portal.forms import EmailValidationOnForgotPassword
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# REST
#from rest_framework import routers


#router = routers.DefaultRouter()

#handler404 = 'portal.views.handler404'
#handler500 = 'portal.views.handler500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.user.urls', 'user'), namespace='user')),
    path('', include(('apps.home.urls', 'home'), namespace='home')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += staticfiles_urlpatterns()
