"""Defines the URL patterns for the users app."""

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'users'

urlpatterns = [
    # Login page
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),

    # Logout page
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # Registration page
    path('register/', views.register, name='register'),
]