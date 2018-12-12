"""
created by:     Django
Description: Tests file for the providers module
Modified by: Fátima
Modify date: 21-11-18
"""

import datetime
from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from franchise.models import Franchise
from provider.models import Provider, OfficeHours
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Order, OrderProductStatus, OrderProductInStatus, OrderStatus, OrderInStatus
import datetime


def create_groups():
    """
    Function for creating the groups/roles of the system
    """
    Group.objects.create(name = "Administrador de empresa")
    Group.objects.create(name = "Almacenista")
    Group.objects.create(name = "Dueño de franquicia")
    Group.objects.create(name = "Empleado generico")
    Group.objects.create(name = "Gerente de compras")
    Group.objects.create(name = "Secretario")


def create_user_provider():
    """
    Function for creating a user in case it is needed
    in the test cases
    """
    nu = User(username='uname')
    nu.set_password('testpasswd123')
    nu.save()
    g = Group.objects.get(name='Administrador de empresa')
    g.user_set.add(nu)
    g.save()
    nup = User.objects.get(username="uname")
    np = Provider(id = 1, id_usuario = nup, activo = True, fecha_registro=timezone.now())
    np.save()
    prov = Provider.objects.get(id = 1)
    ocsUser = OCSUser(user=nu, id_provider = prov)
    ocsUser.save()

def create_user_franchise():
    """
        Function for creating a user in case it is needed
        in the test cases
    """
    nu = User(username='uname2')
    nu.set_password('testpasswd123')
    nu.save()
    g = Group.objects.get(name='Dueño de franquicia')
    g.user_set.add(nu)
    g.save()
    nuf = User.objects.get(username='uname2')
    nf = Franchise(id=1, nombre = "Franquicia", id_usuario=nuf, activo=True, fecha_registro=timezone.now())
    nf.save()
    fran = Franchise.objects.get(id = 1)
    ocsUser = OCSUser(user=nu, id_franchise = fran)
    ocsUser.save()

def create_user_secretary():
    """
        Function for creating a secretary employee in case it is
        needed in the test cases
    """
    nu = User(username='uname4')
    nu.set_password('testpasswd123')
    nu.save()
    g = Group.objects.get(name='Secretario')
    g.user_set.add(nu)
    g.save()
    prov = Provider.objects.get(id = 1)
    ocsUser = OCSUser(user=nu, id_provider = prov)
    ocsUser.save()


def make_order_status():
    one = OrderStatus.objects.create(id = 1, nombre = 'Guardado', activo = True)
    two = OrderStatus.objects.create(id = 2, nombre = 'Pedido', activo = True)
    one = OrderStatus.objects.create(id = 3, nombre = 'Aceptado', activo = True)
    one = OrderStatus.objects.create(id = 4, nombre = 'Rechazado', activo = True)
    one = OrderStatus.objects.create(id = 5, nombre = 'Cancelado', activo = True)
    one = OrderStatus.objects.create(id = 6, nombre = 'En preparacion/enviado', activo = True)
    one = OrderStatus.objects.create(id = 7, nombre = 'Incompleto', activo = True)
    one = OrderStatus.objects.create(id = 8, nombre = 'Completado', activo = True)


def make_order():
    """
        Function for creating an order
    """
    prov = Provider.objects.get(id = 1)
    fran = Franchise.objects.get(id = 1)
    status = OrderStatus.objects.get(id = 2) #init state for these test cases is "Pedido" (2)
    order = Order.objects.create(id = 1, id_franchise = fran, id_provider = prov, fecha_pedido = timezone.now(),
                    fecha_ideal = timezone.now(), fecha_final = timezone.now(), cantidad_productos = 3, precio_total = 10.00,
                    activo = True, arrive = True)

    order_in_status = OrderInStatus.objects.create(id_pedido = order, id_status = status, fecha = timezone.now(), activo = True)

class OrderTests(TestCase):
    def setUp(self):
        create_groups()
        create_user_provider()
        create_user_franchise()
        create_user_secretary()
        make_order_status()
        make_order()

    def test_view_order_main_true(self):
         """
             Only the owner and secretary will be able to consult the order state
         """
         login = self.client.login(username="uname", password="testpasswd123") #login as owner
         response = self.client.get("/orders/consult_orders/")
         self.assertEqual(response.status_code, 200)

         login = self.client.login(username="uname4", password="testpasswd123") #login as the secretary
         response = self.client.get("/orders/consult_orders/")
         self.assertEqual(response.status_code, 200)

    def test_view_order_main_false(self):
         """
             Only the owner and the secretary will be able to consult the order state others will be redirected
         """
         login = self.client.login(username="uname2", password="testpasswd123") #login as a franchise manager
         response = self.client.get("/orders/consult_orders/")
         self.assertNotEqual(response.status_code, 200)

    def test_view_order_detail_true(self):
         """
             Only the owner and the secretary will be able to consult each order detail
         """
         login = self.client.login(username="uname", password="testpasswd123") #login as owner
         prov = Provider.objects.get(id = 1)
         order = Order.objects.get(id_provider = prov)
         id = order.id
         url = "/orders/order_detail/" + str(id) + "/"
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200)

    def test_view_order_detail_false(self):
         """
             Only the owner and the secretary will be able to consult each order detail others will be redirected
         """
         login = self.client.login(username="uname2", password="testpasswd123") #login as a franchise manager
         prov = Provider.objects.get(id = 1)
         order = Order.objects.get(id_provider = prov)
         id = order.id
         url = "/orders/order_detail/" + str(id) + "/"
         response = self.client.get(url)
         self.assertNotEqual(response.status_code, 200)

    def test_modify_order_state_owner(self):
         """
             The owner will be able to modify the order state from "pedido" to "aceptado"
         """
         login = self.client.login(username="uname", password="testpasswd123") #login as owner
         prov = Provider.objects.get(id = 1)
         order = Order.objects.get(id_provider = prov)
         status = OrderStatus.objects.get(id = 3)

         id = order.id
         url = "/orders/order_detail/" + str(id) + "/"
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200)

         order_in = OrderInStatus.objects.get(id_pedido = order)
         final_status = order_in.id_status

         if final_status == status:
             self.assertTrue(True)
         else:
             self.assertTrue(False)

    def test_modify_order_state_secretary(self):
         """
             The secretary will be able to modify the order state from "pedido" to "aceptado"
         """
         login = self.client.login(username="uname4", password="testpasswd123") #login as a secretary
         prov = Provider.objects.get(id = 1)
         order = Order.objects.get(id_provider = prov)
         status = OrderStatus.objects.get(id = 3)

         id = order.id
         url = "/orders/order_detail/" + str(id) + "/"
         response = self.client.get(url)
         self.assertEqual(response.status_code, 200)

         order_in = OrderInStatus.objects.get(id_pedido = order)
         final_status = order_in.id_status

         if final_status == status:
             self.assertTrue(True)
         else:
             self.assertTrue(False)





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
