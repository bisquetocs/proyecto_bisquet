from django.urls import path, include
from . import views

app_name = 'provider'
urlpatterns = [
    path('register', views.registerProvider, name='register'),
    path('infoProvider', views.infoProvider, name='infoProvider'),
    #path('franchise', include('franchise.urls')),
]
