"""
created by:     Django
description:    This are the models of the db for the orders
modify by:      Alberto
modify date:    04/11/18
"""
# Create your models here.
import datetime
from django.db import models
from django.utils import timezone

from provider.models import Provider
from franchise.models import Franchise
from products.models import CompleteProduct
from products.models import UnidadDeMedida

class Order(models.Model):
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    id_provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField('date published')
    fecha_ideal = models.DateTimeField()
    fecha_final = models.DateTimeField(null=True)
    cantidad_productos = models.IntegerField(null=True)
    precio_total = models.DecimalField(max_digits=8 ,decimal_places=3, null=True)
    activo = models.BooleanField()
    arrive = models.BooleanField()

# Estado de un producto en ese pedido (incompleto, mal estado, completo...)
class OrderProductStatus(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, null=True)
    activo = models.BooleanField(default=True)

class OrderProductInStatus(models.Model):
    id_pedido = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_complete_product = models.ForeignKey(CompleteProduct, on_delete=models.CASCADE)
    id_unidad = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE, null=True, default=None)
    cantidad = models.DecimalField(max_digits=6 ,decimal_places=2)
    precio_por_unidad = models.DecimalField(max_digits=6 ,decimal_places=2)
    total = models.DecimalField(max_digits=8 ,decimal_places=3)
    # DATOS UTILES PARA EL CAMBIO DE ESTADOS
    id_status = models.ForeignKey(OrderProductStatus, on_delete=models.CASCADE, null=True)
    comentario = models.CharField(max_length=200, null=True)
    fecha = models.DateTimeField('date published')
    activo = models.BooleanField()

class OrderStatus(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200, null=True)
    activo = models.BooleanField()

class OrderInStatus(models.Model):
    id_pedido = models.ForeignKey(Order, on_delete=models.CASCADE)
    id_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=200, null=True)
    fecha = models.DateTimeField('date published')
    activo = models.BooleanField()
