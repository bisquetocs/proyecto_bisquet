from django import forms
from franchise.models import Franchise
from django.utils import timezone

class RegisterFranchiseForm(forms.Form):
    razon_social = forms.CharField(label='Razón social', max_length=200)
    rfc = forms.CharField(label='RFC', max_length=13)
    nombre = forms.CharField(label='Nombre', max_length=100)
    domicilio = forms.CharField(label='Domicilio', max_length=200)
    def process_registration(self, user):
        p = Franchise(razon_social=self.data['razon_social'],
                        rfc=self.data['rfc'],
                        nombre=self.data['nombre'],
                        domicilio=self.data['domicilio'],
                        activo=True,
                        fecha_registro=timezone.now(),
                        id_usuario=user)
        p.save()
        return 'Registro exitoso'
