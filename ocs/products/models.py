"""
created by:     Django
description:    This are the models of the db
modify by:      Alberto
modify date:    26/10/18
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
