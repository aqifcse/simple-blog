from django.urls import path

from .views import ( 
    UserHomeView, 
    HomeView,
    Contact,
    About 
)

app_name = 'home'

urlpatterns = [
    path('user-home/', UserHomeView.as_view(), name = 'user-home'),
    path('', HomeView.as_view(), name = 'home'),
    path('contact/', Contact.as_view(), name = 'contact'),
    path('about/', About.as_view(), name = 'about')
]