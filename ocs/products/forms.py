from django import forms
from products.models import Product
from django.utils import timezone

class RegisterProductForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }))
    descripcion = forms.CharField(label='Descripción', max_length=200,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }))
    codigo = forms.CharField(label='Código', max_length=10,
        widget=forms.TextInput(
            attrs={
                'class':'form-control',
            }))
    def process_registration(self, Provider):
        p = Product(id_provider=Provider,
                        nombre=self.data['nombre'],
                        descripcion=self.data['descripcion'],
                        codigo=self.data['codigo'],
                        activo=True,
                        fecha_registro=timezone.now())
        p.save()
        return 'Registro exitoso'
