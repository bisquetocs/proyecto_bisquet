from django.urls import path

from . import views

app_name = 'empleados'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registrar/', self.registra_empresa),

]
