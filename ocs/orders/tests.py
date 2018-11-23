"""
Description: Tests file for the orders module
Modified by: Alberto
Modify date: 22-11-18
"""

import datetime
from django.contrib.auth.models import User, Group
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse

from accounts.models import *
from franchise.models import *
from inventory.models import *
from orders.models import *
from products.models import *
from provider.models import *

"""
py manage.py test orders.tests.BetoTestOrders
"""
class BetoTestOrdersViewing(TestCase):
    def test_make_order_view(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        fran = Franchise.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de franquicia",
                                                domicilio= "domicilio",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_franchise=fran)
        myuser.save()
        fran.save()
        ocs_user.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.get('/orders/make_order/')
        self.assertContains(response, "Realiza un pedido:", count=1, status_code=200, msg_prefix='', html=True)

    def test_make_order_to_view(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        fran = Franchise.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de franquicia",
                                                domicilio= "domicilio",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_franchise=fran)
        prov = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de provider",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        myuser.save()
        fran.save()
        ocs_user.save()
        prov.save()
        link = LinkWithF.objects.create(id_provider = prov,
                                        id_franchise = fran,
                                        link_code = 'ABCDEFGHIJKL',
                                        active = True,
                                        used = True,
                                        date_of_creation = timezone.now())
        link.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.get('/orders/make_order/1/')
        self.assertContains(response, "nombre de provider", count=None,status_code=200, msg_prefix='', html=True)

class BetoTestOrdersCreating(TestCase):
    def test_add_product_to_order_without_order(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        fran = Franchise.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de franquicia",
                                                domicilio= "domicilio",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_franchise=fran)
        prov2 = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de provider",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        myuser.save()
        fran.save()
        ocs_user.save()
        prov2.save()
        link = LinkWithF.objects.create(id_provider = prov2,
                                        id_franchise = fran,
                                        link_code = 'ABCDEFGHIJKL',
                                        active = True,
                                        used = True,
                                        date_of_creation = timezone.now())
        link.save()
        product = Product.objects.create(id_provider = prov2,
                                            nombre = 'producto uno',
                                            descripcion = 'un producto equis',
                                            codigo = 'PRUNO',
                                            activo = True,
                                            fecha_registro = timezone.now())
        product.save()
        price = Price.objects.create(id_product = product,
                                        fecha_inicio = timezone.now(),
                                        fecha_final = None,
                                        cantidad = 100,
                                        activo = True)
        price.save()
        umedida = UnidadDeMedida.objects.create(nombre =  'kilos',
                                                abreviacion = 'KG')
        umedida.save()
        complete = CompleteProduct.objects.create(id_product = product,
                                                    id_unidad = umedida,
                                                    id_price = price,
                                                    activo = True)
        complete.save()
        order_s = OrderStatus.objects.create(nombre = 'Guardado',
                                            descripcion = 'guardado',
                                            activo = True)
        order_s.save()

        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.get('/orders/add_product_to_order/', {'id_pedido':'',
                                                                    'id_provider':'1',
                                                                    'nombre_producto':'producto uno',
                                                                    'ud_medida':'1',
                                                                    'cantidad_pedida':'19',
                                                                    'date':'2018-11-28 11:59',})
        exists = Order.objects.filter(id=1).exists()
        self.assertTrue(exists)
        order = Order.objects.get(id=1)
        exists = OrderProductInStatus.objects.filter(id_pedido=order).exists()
        self.assertTrue(exists)
        order_product = OrderProductInStatus.objects.get(id_pedido=order)
        self.assertEqual(product.id, order_product.id_complete_product.id_product.id)

class BetoTestOrdersAdding(TestCase):
    def test_add_product_to_order_with_order(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        fran = Franchise.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de franquicia",
                                                domicilio= "domicilio",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_franchise=fran)
        prov2 = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de provider",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        myuser.save()
        fran.save()
        ocs_user.save()
        prov2.save()
        link = LinkWithF.objects.create(id_provider = prov2,
                                        id_franchise = fran,
                                        link_code = 'ABCDEFGHIJKL',
                                        active = True,
                                        used = True,
                                        date_of_creation = timezone.now())
        link.save()
        product = Product.objects.create(id_provider = prov2,
                                            nombre = 'producto uno',
                                            descripcion = 'un producto equis',
                                            codigo = 'PRUNO',
                                            activo = True,
                                            fecha_registro = timezone.now())
        product.save()
        price = Price.objects.create(id_product = product,
                                        fecha_inicio = timezone.now(),
                                        fecha_final = None,
                                        cantidad = 100,
                                        activo = True)
        price.save()
        umedida = UnidadDeMedida.objects.create(nombre =  'kilos',
                                                abreviacion = 'KG')
        umedida.save()
        complete = CompleteProduct.objects.create(id_product = product,
                                                    id_unidad = umedida,
                                                    id_price = price,
                                                    activo = True)
        complete.save()
        order_s = OrderStatus.objects.create(nombre = 'Guardado',
                                            descripcion = 'guardado',
                                            activo = True)
        order_s.save()
        order = Order.objects.create(id_franchise = fran,
                                        id_provider = prov2,
                                        fecha_pedido = timezone.now(),
                                        fecha_ideal = timezone.now(),
                                        fecha_final = None,
                                        cantidad_productos = 0,
                                        precio_total = 0,
                                        activo = True,
                                        arrive = False)
        order.save()
        order_in_s = OrderInStatus.objects.create(id_pedido = order,
                                                    id_status = order_s,
                                                    comentario = '',
                                                    fecha = timezone.now(),
                                                    activo = True)

        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.get('/orders/add_product_to_order/', {'id_pedido':'1',
                                                                    'id_provider':'1',
                                                                    'nombre_producto':'producto uno',
                                                                    'ud_medida':'1',
                                                                    'cantidad_pedida':'19',
                                                                    'date':'2018-11-28 11:59',})
        exists = Order.objects.filter(id=1).exists()
        self.assertTrue(exists)
        order = Order.objects.get(id=1)
        exists = OrderProductInStatus.objects.filter(id_pedido=order).exists()
        self.assertTrue(exists)
        order_product = OrderProductInStatus.objects.get(id_pedido=order)
        self.assertEqual(product.id, order_product.id_complete_product.id_product.id)
        self.assertEqual(1, order.cantidad_productos)
        self.assertEqual(19*complete.id_price.cantidad, order.precio_total)

class BetoTestOrdersDeleting(TestCase):
    def test_delete_product_from_order(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        fran = Franchise.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de franquicia",
                                                domicilio= "domicilio",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_franchise=fran)
        prov2 = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de provider",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        myuser.save()
        fran.save()
        ocs_user.save()
        prov2.save()
        link = LinkWithF.objects.create(id_provider = prov2,
                                        id_franchise = fran,
                                        link_code = 'ABCDEFGHIJKL',
                                        active = True,
                                        used = True,
                                        date_of_creation = timezone.now())
        link.save()
        product = Product.objects.create(id_provider = prov2,
                                            nombre = 'producto uno',
                                            descripcion = 'un producto equis',
                                            codigo = 'PRUNO',
                                            activo = True,
                                            fecha_registro = timezone.now())
        product.save()
        price = Price.objects.create(id_product = product,
                                        fecha_inicio = timezone.now(),
                                        fecha_final = None,
                                        cantidad = 100,
                                        activo = True)
        price.save()
        umedida = UnidadDeMedida.objects.create(nombre =  'kilos',
                                                abreviacion = 'KG')
        umedida.save()
        complete = CompleteProduct.objects.create(id_product = product,
                                                    id_unidad = umedida,
                                                    id_price = price,
                                                    activo = True)
        complete.save()
        order_s = OrderStatus.objects.create(nombre = 'Guardado',
                                            descripcion = 'guardado',
                                            activo = True)
        order_s.save()
        order = Order.objects.create(id_franchise = fran,
                                        id_provider = prov2,
                                        fecha_pedido = timezone.now(),
                                        fecha_ideal = timezone.now(),
                                        fecha_final = None,
                                        cantidad_productos = 0,
                                        precio_total = 0,
                                        activo = True,
                                        arrive = False)
        order.save()
        order_in_s = OrderInStatus.objects.create(id_pedido = order,
                                                    id_status = order_s,
                                                    comentario = '',
                                                    fecha = timezone.now(),
                                                    activo = True)

        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.get('/orders/add_product_to_order/', {'id_pedido':'1',
                                                                    'id_provider':'1',
                                                                    'nombre_producto':'producto uno',
                                                                    'ud_medida':'1',
                                                                    'cantidad_pedida':'19',
                                                                    'date':'2018-11-28 11:59',})
        exists = Order.objects.filter(id=1).exists()
        self.assertTrue(exists)
        order = Order.objects.get(id=1)
        exists = OrderProductInStatus.objects.filter(id_pedido=order).exists()
        self.assertTrue(exists)
        order_product = OrderProductInStatus.objects.get(id_pedido=order)
        self.assertEqual(product.id, order_product.id_complete_product.id_product.id)
        self.assertEqual(1, order.cantidad_productos)
        self.assertEqual(19*complete.id_price.cantidad, order.precio_total)
        response = self.client.get('/orders/delete_product_from_order/', {'id_pedido':'1',
                                                                        'id_prod_ord':'1',})
        order = Order.objects.get(id=1)
        self.assertEqual(0, order.cantidad_productos)
        self.assertEqual(0, order.precio_total)









        #
