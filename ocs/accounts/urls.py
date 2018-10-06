from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.homePage, name='home'),
]
