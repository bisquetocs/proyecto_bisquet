from django.urls import path

from . import views

app_name = 'provider'
urlpatterns = [
    path('register', views.registerProvider, name='register'),
]
