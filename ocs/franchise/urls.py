"""
Created by : Django
Description: URL patterns for the different path on the franchise module
Modified by: Dante F
Modify date: 26-10-18
"""

from django.urls import path, include
from . import views

app_name = 'franchise'
urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.registerFranchise, name='register'),
    path('home/', views.home, name='home'),
    path('my_inventory/', views.show_inventory, name='show_inventory'),
    path('my_providers/', views.my_providers, name='my_providers'),
    path('my_providers/link/', views.link_provider, name='link_provider'),
    path('my_providers/<int:id_provider>', views.provider_detail, name='provider_detail'),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.edit_franchise, name="editProfile"),

]
