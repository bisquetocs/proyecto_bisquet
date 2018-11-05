
"""
created by:     Django
description:    This are the paths that are shown in the browser
                while interacting with products
modify by:      Alberto
modify date:    04/11/18
"""
from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'products'
urlpatterns = [
    path('myProducts/', views.my_products, name='myProducts'),
    path('register/', views.registerProduct, name='register'),

    # FUNCIONES DE AJAX
    path('able_unable_product/', views.able_unable_product, name='able_unable_product'),
    path('get_product/', views.get_product_info, name='get_product'),
    path('edit/', views.edit_product, name='edit'),
    path('get_product_price/', views.get_product_price, name='get_product_price'),
    path('check_unidad/', views.check_unidad, name='check_unidad'),
    path('add_price/', views.add_price, name='add_price'),
    path('save_price/', views.save_price, name='save_price'),
    path('delete_price/', views.delete_price, name='delete_price'),

    path('get_product_equiv/', views.get_product_equiv, name='get_product_equiv'),
    path('add_equivalencia/', views.add_equivalencia, name='add_equivalencia'),

    path('delete_equiv/', views.delete_equiv, name='delete_equiv'),
    path('check_equiv_destino/', views.check_equiv_destino, name='check_equiv_destino'),
]
