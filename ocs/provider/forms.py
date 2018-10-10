from django import forms
from django.utils import timezone

from provider.models import Provider
from accounts.models import OCSUser

class RegisterProviderForm(forms.Form):
    razon_social = forms.CharField(label='Razón social', max_length=200)
    rfc = forms.CharField(label='RFC', max_length=13)
    nombre = forms.CharField(label='Nombre', max_length=100)
    domicilio = forms.CharField(label='Domicilio', max_length=200)
    mision = forms.CharField(label='Misión', max_length=4000)
    vision = forms.CharField(label='Visión', max_length=4000)
    def process_registration(self, user):
        u = OCSUser.objects.get(user = user)
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
        u.id_provider = p
        u.save()
        return 'Registro exitoso'
