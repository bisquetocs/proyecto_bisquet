"""
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



def create_user_franchise():
    """
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
    nf = Franchise(id=1, id_usuario=nu, activo=True, fecha_registro=timezone.now())
    nf.save()

# Create your tests here.
class ProviderViewTest(TestCase):

    def test_non_existing_provider_detail(self):
        """
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
            If the user consults the franchise inventory, and the inventory is
            empty, the system will return a queryset with a len() of 0
        """
        user = create_user_franchise()
        self.client.login(username="uname", password="testpasswd123")
        response = self.client.get('/franchise/my_inventory/')

        self.assertEqual(len(response.context['product_list']), 0)
