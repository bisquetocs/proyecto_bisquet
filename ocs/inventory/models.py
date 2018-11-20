"""
Created by : Django
Description: Models file used to design and create entitites on the database
             for the Inventory module
Modified by: Dante F
Modify date: 1-11-18
"""
import datetime
from django.db import models
from django.utils import timezone
from franchise.models import Franchise
from products.models import Product
from django.contrib.auth.models import User
from products.models import UnidadDeMedida


# Create your models here.
class PrivateProduct(models.Model):
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=8 ,decimal_places=2)
    unit = models.CharField(max_length=100)

class LinkedInventory(models.Model):
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_unidad = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=8 ,decimal_places=2)

class PrivateProductRecord(models.Model):
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    id_private_product = models.ForeignKey(PrivateProduct, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8 ,decimal_places=2)
    io = models.BooleanField() #input-True     Output-False

class LinkedProductRecord(models.Model):
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    id_linked_product = models.ForeignKey(LinkedInventory, on_delete=models.CASCADE)
    id_unidad = models.ForeignKey(UnidadDeMedida, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=8 ,decimal_places=2)
    io = models.BooleanField()
