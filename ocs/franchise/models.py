import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Franchise(models.Model):
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

    def __getattr__(self, attrname):
        aux = self.attrname
        if aux == '' or aux is None:
            return -1
        else:
            return aux
