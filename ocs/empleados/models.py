import datetime
from django.db import models
from django.utils import timezone

class Empresa(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre_empresa

class Privilegio(models.Model):
    nombre_privilegio = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre_privilegio

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre_rol

class RolPrivilegio(models.Model):
    id_Rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    id_Privilegio = models.ForeignKey(Privilegio, on_delete=models.CASCADE)
    def __str__(self):
        return self

class Empleado(models.Model):
    nombre_empleado = models.CharField(max_length=200)
    correo_empleado = models.CharField(max_length=200)
    RFC_empleado = models.CharField(max_length=13)
    id_Empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    id_Rol = models.ForeignKey(Rol, on_delete = models.CASCADE)
    def __str__(self):
        return self.nombre_empleado
