from django.urls import path, include
from . import views

app_name = 'franchise'
urlpatterns = [
    path('register', views.registerFranchise, name='register'),
    path('home', views.home, name='home'),
    path('my_providers/link/', views.link_provider, name='link_provider'),

]
