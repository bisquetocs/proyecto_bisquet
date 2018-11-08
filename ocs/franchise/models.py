"""
Created by : Django
Description: Models file used to design and create entitites on the database
             for the Franchise module
Modified by: Dante F
Modify date: 26-10-18
"""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Franchise(models.Model):
    razon_social = models.CharField(max_length=200)
    rfc = models.CharField(max_length=13)
    nombre = models.CharField(max_length=100)
    domicilio = models.TextField(max_length=200)
    activo = models.BooleanField()
    fecha_registro = models.DateTimeField('date published')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.rfc


# esta debe estar en products... IMPORTANTE
class PrivateProduct(models.Model):
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()
