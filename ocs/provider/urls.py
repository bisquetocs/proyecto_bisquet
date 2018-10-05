from django.urls import path

from . import views

app_name = 'provider'
urlpatterns = [
    path('register', views.RegisterView, name='register'),
    path('registerProvider/', views.registerProvider, name='registerProvider'),
]
