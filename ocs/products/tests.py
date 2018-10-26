from django.test import TestCase, Client
from django.contrib.auth.models import User
from products.models import Product
from provider.models import Provider
import datetime

# Create your tests here.

def createProduct():
    u = User(username='user', is_staff=True)
    prov = Provider(razon_social = 'a',rfc = 'a',nombre = 'a',domicilio = 'a',mision = 'a',vision = 'a',activo = True,fecha_registro = datetime.datetime.now(),id_usuario = u.id)
    prod = Product(id_provider = prov.id, nombre = 'producto', descripcion = 'este es un producto', codigo = 'PROD', activo = True, fecha_registro = datetime.datetime.now())
    return prod

class AddCreateProductTest(TestCase):
    def testAddProduct(self):
        p = createProduct()
        self.assertTrue(isinstance(p,Product))

class EditProductTest(TestCase):
    def testEditProduct(self):
        p = createProduct()
        p.razon_social='b'
        self.assertTrue(p.razon_social,'b')
    def testAbleUnableProduct(self):
        p = createProduct()
        p2 = createProduct()
        p.activo=True
        p2.activo=False
        self.assertTrue(not p2.activo and p.activo)
