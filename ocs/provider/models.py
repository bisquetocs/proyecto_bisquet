"""
created by:     Django
description:    This are our models (db tables) that help us with data control
modify by:      Alberto
modify date:    26/10/18
"""

import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from franchise.models import Franchise

class Provider(models.Model):
    razon_social = models.CharField(max_length=200)
    rfc = models.CharField(max_length=13)
    nombre = models.CharField(max_length=100)
    domicilio = models.TextField(max_length=200)
    mision = models.TextField(max_length=4000)
    vision = models.TextField(max_length=4000)
    activo = models.BooleanField()
    fecha_registro = models.DateTimeField('date published')
    id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.rfc

class LinkWithF(models.Model):
    id_provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, blank=True, null=True)
    link_code = models.CharField(max_length=12)
    active = models.BooleanField()
    used = models.BooleanField()
    date_of_creation = models.DateTimeField(default=timezone.now, blank=True)
    def check_timeout(self):
        if (timezone.now() - self.date_of_creation) > datetime.timedelta(days=5):
            return True
        return False

class Days(models.Model):
    nombre = models.CharField(max_length = 100)
    def __str__(self):
        return self.nombre

class OfficeHours(models.Model):
    id_provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank=True, null=True)
    day = models.ForeignKey(Days, on_delete=models.CASCADE, blank=True, null=True)
    start_hour = models.TimeField()
    finish_hour = models.TimeField()

class DailyClients(models.Model):
    id_provider = models.ForeignKey(Provider, on_delete=models.CASCADE, blank = True, null = True)
    id_franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE, blank = True, null = True)
    day = models.ForeignKey(Days, on_delete = models.CASCADE, blank = True, null = True)
    activo = models.BooleanField()
