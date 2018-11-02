"""
Created by : Django
Description: URL patterns for the different path on the inventory module
Modified by: Dante F
Modify date: 1-11-18
"""

from django.urls import path, include
from . import views

app_name = 'my_inventory'
urlpatterns = [
    path('', views.show_inventory, name='show_inventory'),
    path('register/', views.register_private_product, name='register_private_product'),
    path('create_pdf/', views.create_pdf, name='create_pdf')
]
