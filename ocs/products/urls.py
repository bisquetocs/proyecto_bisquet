from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('myProducts/', views.my_products, name='myProducts'),
    path('register/', views.registerProduct, name='register'),
    path('<int:id_product>/edit/', views.editProduct, name='edit'),
    path('<int:id_product>/ableUnable/', views.ableUnableProduct, name='ableUnable'),

]
