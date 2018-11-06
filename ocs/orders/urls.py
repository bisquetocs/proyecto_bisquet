
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
]
