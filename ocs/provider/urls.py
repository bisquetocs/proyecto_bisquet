from django.urls import path, include
from . import views

app_name = 'provider'
urlpatterns = [
    path('register', views.registerProvider, name='register'),
    path('home', views.home, name='home'),
    
]
