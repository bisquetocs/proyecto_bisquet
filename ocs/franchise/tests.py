"""
Created by : Django
Description: Test file for the Franchise module
Modified by: Dante F
Modify date: 26-10-18
"""

from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from .models import Franchise, PrivateProduct
from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory
from . import views
from django.utils import timezone

def create_user_provider():
    """
    Function for creating a user in case it is needed
    in the test cases
    """
    ng = Group(name='Administrador de empresa')
    ng.save()
    nu = User(username='uname')
    nu.set_password('testpasswd123')
    nu.save()
    g = Group.objects.get(name='Administrador de empresa')
    g.user_set.add(nu)
    g.save()
    ocsUser = OCSUser(user=nu)
    ocsUser.save()

def create_user_franchise():
    """
        By: DanteMaxF
        Function for creating a user in case it is needed
        in the test cases
    """
    ng = Group(name='Dueño de franquicia')
    ng.save()
    nu = User(username='uname')
    nu.set_password('testpasswd123')
    nu.save()
    g = Group.objects.get(name='Dueño de franquicia')
    g.user_set.add(nu)
    g.save()
    ocsUser = OCSUser(user=nu)
    ocsUser.save()
    nf = Franchise( id_usuario=nu,
                    activo=True,
                    fecha_registro=timezone.now(),
                    razon_social='razon_social_test',
                    rfc = 'rfc_test',
                    nombre = 'Los bisquets de obregon',
                    domicilio = 'domicilio test'
                    )
    nf.save()
    ocsUser.id_franchise = nf
    ocsUser.save()

# Create your tests here.
class ProviderViewTest(TestCase):

    def test_non_existing_provider_detail(self):
        """
            By: DanteMaxF
            The detail view of a non existing provider id returns
            a 404 not found
            Since there is no provider registered in the database test,
            any request to that view will be a 404
        """
        # non_existing_provider_id = 4
        user = create_user_franchise()
        self.client.login(username="uname", password="testpasswd123")
        response = self.client.get('/franchise/my_providers/4')
        self.assertEqual(response.status_code, 404)

    def test_empty_provider_catalog(self):
        """
            By: DanteMaxF
            The return of an empty query set when consulting the providers catalog
            results in returning a variable that represents that the list is
            empty
        """
        user = create_user_franchise()
        self.client.login(username="uname", password="testpasswd123")
        response = self.client.get('/franchise/my_providers/')
        self.assertEqual(response.context['empty_list'], 1)


class InventoryTests(TestCase):

    def test_check_inventory_empty(self):
        """
            By: DanteMaxF
            If the user consults the franchise inventory, and the inventory is
            empty, the system will return a queryset with a len() of n products in the
            database
        """
        user = create_user_franchise()
        self.client.login(username="uname", password="testpasswd123")
        gu = User.objects.get(username='uname')
        u = OCSUser.objects.get(user = gu)
        new_product = PrivateProduct(id_franchise=u.id_franchise, name='Brocoli', description='Brocoli cool', amount="10")
        new_product.save()
        response = self.client.get('/franchise/my_inventory/')


        self.assertNotEqual(len(response.context['product_list']), 0)


    def test_user_register_new_product(self):
        """
            If the user post the correct parameters when it registers a private product,
            the new product is going to be uploaded to the database successfully
        """
        create_user_franchise()
        self.client.login(username='uname', password='testpasswd123')
        u = User.objects.get(username='uname')
        ou = OCSUser.objects.get(user = u)

        response = self.client.post('/franchise/my_inventory/register/',  {'product_name': 'Naranja',
                                                                 'product_desc': 'Naranja proveniente de FRUVELOZ',
                                                                 'product_amount': '23'
                                                                 })
        PrivateProduct.objects.get(name='Naranja')

    def test_user_register_new_product_invalid_value(self):
        """
            If the user post some invalid parameters, the system will notify the user
            the invalid parameters that was inserted, and the product will not be uploaded
            to the database
        """
        create_user_franchise()
        self.client.login(username='uname', password='testpasswd123')
        u = User.objects.get(username='uname')
        ou = OCSUser.objects.get(user = u)

        response = self.client.post('/franchise/my_inventory/register/',  {'product_name': 'Brocoli',
                                                                 'product_desc': 'Brocoli',
                                                                 'product_amount': '-23'
                                                                 })
        test_query = PrivateProduct.objects.filter(name='Brocoli')
        self.assertEqual(len(test_query), 0)
