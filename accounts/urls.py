from django.urls import path
from . import views
from .utils import create_admin_once


urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('auth/', views.auth_toggle, name='auth_toggle'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('create-admin/', views.create_admin, name='create_admin'),
]