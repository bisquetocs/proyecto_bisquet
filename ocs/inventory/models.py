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

# Create your models here.
class PrivateProduct(models.Model):
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()

class LinkedInventory(models.Model):
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()
