
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

    path('bloquear_pedido/', views.bloquear_pedido, name='bloquear_pedido'),
    path('desbloquear_pedido/', views.desbloquear_pedido, name='desbloquear_pedido'),
    path('rechazar_pedido/', views.rechazar_pedido, name='rechazar_pedido'),

    path('consult_order_history_prov/', views.consult_order_history_prov, name="consult_order_history_prov"),
    path('consult_order_history_franq/', views.consult_order_history_franq, name="consult_order_history_franq"),
    path('register_arrival/<int:id_order>/', views.register_arrival, name='register_arrival'),

    path('complete_order/', views.complete_order, name='complete_order'),
]
