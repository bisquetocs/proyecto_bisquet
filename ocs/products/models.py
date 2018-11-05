"""
created by:     Django
description:    This are the models of the db
modify by:      Alberto
modify date:    04/11/18
"""
# Create your models here.
import datetime
from django.db import models
from django.utils import timezone
from provider.models import Provider
from franchise.models import Franchise



class Product(models.Model):
    id_provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=200)
    codigo = models.CharField(max_length=10)
    activo = models.BooleanField()
    fecha_registro = models.DateTimeField('date published')
    def __str__(self):
        return self.nombre

class Price(models.Model):
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField('date published')
    fecha_final = models.DateTimeField(null=True)
    cantidad = models.DecimalField(max_digits=6 ,decimal_places=2)
    activo = models.BooleanField()

class UnidadDeMedida(models.Model):
    nombre =  models.CharField(max_length=20)
    abreviacion = models.CharField(max_length=10)

class CompleteProduct(models.Model):
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_unidad = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE)
    id_price = models.ForeignKey(Price, on_delete=models.CASCADE)
    activo = models.BooleanField()

class Equivalencias(models.Model):
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_unidad_origen = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE, related_name='id_unidad_origen')
    cantidad_origen = models.DecimalField(max_digits=6 ,decimal_places=2, default=1)
    id_unidad_destino = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE, related_name='id_unidad_destino')
    cantidad_destino = models.DecimalField(max_digits=6 ,decimal_places=2)
    activo = models.BooleanField()








#
