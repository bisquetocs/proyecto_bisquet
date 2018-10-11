from django.urls import path

from . import views

app_name = 'franchise'
urlpatterns = [
    path('register', views.registerFranchise, name='register'),
]
