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


class LinkedInventory(models.Model):
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
