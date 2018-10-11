from django import forms
from django.utils import timezone

from franchise.models import Franchise
from accounts.models import OCSUser

class RegisterFranchiseForm(forms.Form):
    razon_social = forms.CharField(label='Razón social', max_length=200,
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'2',
            }))
    rfc = forms.CharField(label='RFC', max_length=13,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }))
    nombre = forms.CharField(label='Nombre', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }))
    domicilio = forms.CharField(label='Domicilio', max_length=200,
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'2',
            }))
    def process_registration(self, user):
        u = OCSUser.objects.get(user = user)
        f = Franchise(razon_social=self.data['razon_social'],
                        rfc=self.data['rfc'],
                        nombre=self.data['nombre'],
                        domicilio=self.data['domicilio'],
                        activo=True,
                        fecha_registro=timezone.now(),
                        id_usuario=user)
        f.save()
        u.id_franchise = f.id
        u.save()
        return 'Registro exitoso'
