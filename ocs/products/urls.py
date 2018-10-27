
"""
created by:     Django
description:    This are the paths that are shown in the browser
                while interacting with products
modify by:      Alberto
modify date:    26/10/18
"""
from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('myProducts/', views.my_products, name='myProducts'),
    path('register/', views.registerProduct, name='register'),
    path('edit/<int:id_product>/', views.editProduct, name='edit'),
    path('ableUnable/<int:id_product>/', views.ableUnableProduct, name='ableUnable'),
]
