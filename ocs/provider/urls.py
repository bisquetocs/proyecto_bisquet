from django.urls import path, include
from . import views

app_name = 'provider'
urlpatterns = [
    path('register/', views.registerProvider, name='register'),
    path('home/', views.home, name='home'),
    path('my_clients/link_code/', views.link_code, name='link_code'),
    path('office/', views.office, name='office'),
    path('clients/', views.clients, name='clients'),
    path('clients/daily_clients', views.daily_clients, name='daily_clients')

]
