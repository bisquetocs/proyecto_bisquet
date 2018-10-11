from django import forms
from products.models import Product
from django.utils import timezone

class RegisterProductForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    descripcion = forms.CharField(label='Descripción', max_length=200)
    def process_registration(self, Product):
        p = Product(id_proveedor=Product,
                        nombre=self.data['nombre'],
                        descripcion=self.data['descripcion'],
                        activo=True,
                        fecha_registro=timezone.now())
        p.save()
        return 'Registro exitoso'
