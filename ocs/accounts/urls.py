from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.forms import UserCreationForm


urlpatterns = [
    path('register/', views.register, name='register'),
    path('register/check', views.registerUser, name='registerUser'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('', views.home, name='home'),
]
