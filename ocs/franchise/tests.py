from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from django.test import TestCase
from django.urls import reverse
from django.test.client import RequestFactory
from . import views


def create_user():
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

# Create your tests here.
class ProviderDetailViewTest(TestCase):

    def test_non_existing_provider_high_number(self):
        """
        The detail view of a non existing provider id returns
        a 404 not found
        Since there is no provider registered in the database test,
        any request to that view will be a 404
        """
        # non_existing_provider_id = 4
        user = create_user()
        self.client.login(username="uname", password="testpasswd123")
        response = self.client.get('/franchise/my_providers/4')
        print("The response code obtained is: "+str(response.status_code))
        self.assertEqual(response.status_code, 404)
