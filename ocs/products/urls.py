from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('register', views.registerProduct, name='register'),
]
