from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth.forms import UserCreationForm

#app_name = 'accounts'
urlpatterns = [
    path('', views.home, name='home'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('locate/', views.locate, name='locate'),
    path('myEmployees/', views.misEmpleados, name='myEmployees'),
    path('myEmployees/delete/<int:emp_id>', views.borrarEmpleado, name='delete'),
    path('linkEmployee/', views.registrarEmpleado, name='linkEmployee'),

]
