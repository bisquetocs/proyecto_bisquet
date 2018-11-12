
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

app_name = 'orders'
urlpatterns = [
    path('make_order/', views.make_order, name='make_order'),
    path('make_order/<int:id_provider>/', views.make_order_to, name='make_order_to'),
    path('add_product_to_order/', views.add_product_to_order, name='add_product_to_order'),
    path('delete_product_from_order/', views.delete_product_from_order, name='delete_product_from_order'),
    path('consult_orders/', views.consult_orders, name="consult_orders"),
    path('order_detail/<int:id_order>/', views.order_detail, name='order_detail'),
    path('cancel_order/', views.cancel_order, name='cancel_order'),
    path('send_order/', views.send_order, name='send_order'),

]
