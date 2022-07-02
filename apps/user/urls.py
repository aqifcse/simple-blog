from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework import routers

from .views import ( 
    UserRegistrationView,
    ActivateAccount,
    UserLoginView,
    DashboardAdminView,
    AdminUserList,
    AdminCategoryList,
    AdminCategoryAdd,
    AdminNewsAdd,
    AdminNewsList,
    AdminNewsByCategoryList,
    UserDeleteAPIView
)

router = routers.DefaultRouter()

app_name = 'user'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(template_name='users/login.html'), name='login'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('admin-login/', UserLoginView.as_view(template_name='users/admin_login.html'), name='admin-login'),
    path('portal-admin/', DashboardAdminView.as_view(), name='portal-admin'),
    path('admin-user-list/', AdminUserList.as_view(), name='admin-user-list'),
    path('admin-category-list/', AdminCategoryList.as_view(), name='admin-category-list'),
    path('admin-news-list/', AdminNewsList.as_view(), name='admin-news-list'),
    path('admin-news-by-category/<slug:category_slug>/', AdminNewsByCategoryList.as_view(), name='admin-news-by-category'),
    path('admin-category-add/', AdminCategoryAdd.as_view(), name='admin-category-add'),
    path('admin-news-add/', AdminNewsAdd.as_view(), name='admin-news-add'),
    path('user-delete-api/<email>/delete/', UserDeleteAPIView.as_view(), name='user_delete_api'),
]