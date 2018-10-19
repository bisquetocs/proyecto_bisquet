from django.urls import path, include
from . import views

app_name = 'provider'
urlpatterns = [
    path('register/', views.registerProvider, name='register'),
    path('home/', views.home, name='home'),
    path('my_client/', views.my_client, name='my_client'),
    path('my_clients/link_code/', views.link_code, name='link_code'),
    path('office/', views.office, name='office'),

]
