from django.urls import path

from . import views

app_name = 'empleados'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registro/', views.RegisterView.as_view(), name='registro'),
    path('vote/', views.vote, name='vote'),


]
