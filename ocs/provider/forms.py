"""
created by:     Django
description:    This are the forms we use to providers
modify by:      Alberto
modify date:    26/10/18
"""

from django import forms
from django.utils import timezone

from provider.models import Provider
from accounts.models import OCSUser
from django.contrib.auth.models import User, Group

class RegisterProviderForm(forms.Form):

    razon_social = forms.CharField(label='Razón social',max_length=200,
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
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }))
    mision = forms.CharField(label='Misión', max_length=4000,
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'3',
            }))
    vision = forms.CharField(label='Visión', max_length=4000,
        widget=forms.Textarea(
            attrs={
                'class':'form-control',
                'rows':'3',
            }))
    #input, desc, output
    def process_registration(self, user):
        u = user
        ocsu = OCSUser.objects.get(user = user)
        p = Provider(razon_social=self.data['razon_social'],
                        rfc=self.data['rfc'],
                        nombre=self.data['nombre'],
                        domicilio=self.data['domicilio'],
                        mision=self.data['mision'],
                        vision=self.data['vision'],
                        activo=True,
                        fecha_registro=timezone.now(),
                        id_usuario=user)
        p.save()
        ocsu.id_provider = p
        ocsu.save()
        g = Group.objects.get(name="Administrador de empresa")
        g.user_set.add(u)
        g.save()
        return p
