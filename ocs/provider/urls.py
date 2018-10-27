"""
created by:     Django
description:    This are the paths of the providers app to show in the browser
                This paths lead to our views
modify by:      Alberto
modify date:    25/10/18
"""

from django.urls import path, include
from . import views

app_name = 'provider'
urlpatterns = [
    path('register/', views.registerProvider, name='register'),
    path('home/', views.home, name='home'),
    path('my_clients/', views.my_clients, name='my_clients'),
    path('my_clients/link_code/', views.link_code, name='link_code'),
    path('office/', views.office, name='office'),
    path('my_clients/<int:id_franchise>', views.client_detail, name='client_detail'),
    path('my_clients/daily_clients', views.daily_clients, name='daily_clients'),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.edit_provider, name="editProfile"),
]
