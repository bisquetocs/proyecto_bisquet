"""
Created by : Django
Description: Test file for the Franchise module
Modified by: Dante F
Modify date: 26-10-18
"""

from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from .models import Franchise
from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory
from . import views
from django.utils import timezone
from inventory.models import PrivateProduct, PrivateProductRecord

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


class TestsInventory(TestCase):
    # OUTPUT
    def test_user_register_product_output_with_negative_amount(self):
        """
            If the user tries to resgister an output of a product, and the amount
            is a negative value , the registration will fail
        """
        create_user_franchise()
        self.client.login(username='uname', password='testpasswd123')
        u = User.objects.get(username='uname')
        ou = OCSUser.objects.get(user = u)
        response = self.client.post('/franchise/my_inventory/register/',  {'product_name': 'Naranja',
                                                                 'product_desc': 'Naranja proveniente de FRUVELOZ',
                                                                 'product_amount': 23,
                                                                 'product_unit': 'KG'
                                                                 })
        pp = PrivateProduct.objects.get(name='Naranja')

        response = self.client.post('/franchise/my_inventory/update_private_product/', {
                                                                                        'id_product': pp.id,
                                                                                        'product_io': 'out',
                                                                                        'product_amount': -1,
                                                                                        'product_comment': 'comment'
                                                                                        })
        pp2 = PrivateProduct.objects.get(name='Naranja')
        self.assertEqual(pp2.amount, 23)

    def test_user_register_product_output_more_than_the_inventory_has(self):
        """
            If the user tries to resgister an output of a product, and the amount
            is bigger than what they have on the inventory, the registration will
            fail
        """
        create_user_franchise()
        self.client.login(username='uname', password='testpasswd123')
        u = User.objects.get(username='uname')
        ou = OCSUser.objects.get(user = u)
        response = self.client.post('/franchise/my_inventory/register/',  {'product_name': 'Naranja',
                                                                 'product_desc': 'Naranja proveniente de FRUVELOZ',
                                                                 'product_amount': 23,
                                                                 'product_unit': 'KG'
                                                                 })
        pp = PrivateProduct.objects.get(name='Naranja')

        response = self.client.post('/franchise/my_inventory/update_private_product/', {
                                                                                        'id_product': pp.id,
                                                                                        'product_io': 'out',
                                                                                        'product_amount': 25,
                                                                                        'product_comment': 'comment'
                                                                                        })
        pp2 = PrivateProduct.objects.get(name='Naranja')
        self.assertEqual(pp2.amount, 23)

    def test_user_register_a_correct_output(self):
        """
            If the user tries to register an output of a product, and it passess
            all the parameters, the registration will continue in a correct way
        """
        create_user_franchise()
        self.client.login(username='uname', password='testpasswd123')
        u = User.objects.get(username='uname')
        ou = OCSUser.objects.get(user = u)
        response = self.client.post('/franchise/my_inventory/register/',  {'product_name': 'Naranja',
                                                                 'product_desc': 'Naranja proveniente de FRUVELOZ',
                                                                 'product_amount': 23,
                                                                 'product_unit': 'KG'
                                                                 })
        pp = PrivateProduct.objects.get(name='Naranja')

        response = self.client.post('/franchise/my_inventory/update_private_product/', {
                                                                                        'id_product': pp.id,
                                                                                        'product_io': 'out',
                                                                                        'product_amount': 2,
                                                                                        'product_comment': 'comment'
                                                                                        })
        pp2 = PrivateProduct.objects.get(name='Naranja')
        self.assertEqual(pp2.amount, 21)


    # INPUT
    def test_user_register_product_input_with_negative_amount(self):
        """
            If the user tries to resgister an input of a product, and the amount
            is a negative value , the registration will fail
        """
        create_user_franchise()
        self.client.login(username='uname', password='testpasswd123')
        u = User.objects.get(username='uname')
        ou = OCSUser.objects.get(user = u)
        response = self.client.post('/franchise/my_inventory/register/',  {'product_name': 'Naranja',
                                                                 'product_desc': 'Naranja proveniente de FRUVELOZ',
                                                                 'product_amount': 23,
                                                                 'product_unit': 'KG'
                                                                 })
        pp = PrivateProduct.objects.get(name='Naranja')

        response = self.client.post('/franchise/my_inventory/update_private_product/', {
                                                                                        'id_product': pp.id,
                                                                                        'product_io': 'in',
                                                                                        'product_amount': -1,
                                                                                        'product_comment': 'comment'
                                                                                        })
        pp2 = PrivateProduct.objects.get(name='Naranja')
        self.assertEqual(pp2.amount, 23)

    def test_user_register_a_correct_input(self):
        """
            If the user tries to register an output of a product, and it passess
            all the parameters, the registration will continue in a correct way
        """
        create_user_franchise()
        self.client.login(username='uname', password='testpasswd123')
        u = User.objects.get(username='uname')
        ou = OCSUser.objects.get(user = u)
        response = self.client.post('/franchise/my_inventory/register/',  {'product_name': 'Naranja',
                                                                 'product_desc': 'Naranja proveniente de FRUVELOZ',
                                                                 'product_amount': 23,
                                                                 'product_unit': 'KG'
                                                                 })
        pp = PrivateProduct.objects.get(name='Naranja')

        response = self.client.post('/franchise/my_inventory/update_private_product/', {
                                                                                        'id_product': pp.id,
                                                                                        'product_io': 'in',
                                                                                        'product_amount': 2,
                                                                                        'product_comment': 'comment'
                                                                                        })
        pp2 = PrivateProduct.objects.get(name='Naranja')
        self.assertEqual(pp2.amount, 25)

    def test_user_miss_a_comment(self):
        """
            If the user tries to register an input/output of a product, and the user
            misses to introduce a comment, the registration will fail
        """
        create_user_franchise()
        self.client.login(username='uname', password='testpasswd123')
        u = User.objects.get(username='uname')
        ou = OCSUser.objects.get(user = u)
        response = self.client.post('/franchise/my_inventory/register/',  {'product_name': 'Naranja',
                                                                 'product_desc': 'Naranja proveniente de FRUVELOZ',
                                                                 'product_amount': 23,
                                                                 'product_unit': 'KG'
                                                                 })
        pp = PrivateProduct.objects.get(name='Naranja')

        response = self.client.post('/franchise/my_inventory/update_private_product/', {
                                                                                        'id_product': pp.id,
                                                                                        'product_io': 'in',
                                                                                        'product_amount': 1,
                                                                                        'product_comment': ''
                                                                                        })
        pp2 = PrivateProduct.objects.get(name='Naranja')
        self.assertEqual(pp2.amount, 23)

    def test_see_ios(self):
        """
            If the user sends a request for the inputs and outputs records, the system will display
            the reports of all the inputs and outputs that had been made in the user's franchise
        """
        create_user_franchise()
        self.client.login(username='uname', password='testpasswd123')
        u = User.objects.get(username='uname')
        ou = OCSUser.objects.get(user = u)
        response = self.client.post('/franchise/my_inventory/register/',    {
                                                                            'product_name': 'Naranja',
                                                                            'product_desc': 'Naranja proveniente de FRUVELOZ',
                                                                            'product_amount': 23,
                                                                            'product_unit': 'KG'
                                                                            })
        pp = PrivateProduct.objects.get(name='Naranja')

        response = self.client.post('/franchise/my_inventory/update_private_product/', {
                                                                                        'id_product': pp.id,
                                                                                        'product_io': 'in',
                                                                                        'product_amount': 2,
                                                                                        'product_comment': 'comment'
                                                                                        })

        record_list = PrivateProductRecord.objects.filter(id_franchise=ou.id_franchise)
        self.assertEqual(len(record_list), 2)
