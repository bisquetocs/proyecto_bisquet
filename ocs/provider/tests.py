"""
created by:     Django
description:    This are the tests to ensure that our functionalities works fine
modify by:      Alberto
modify date:    26/10/18
"""

import datetime
from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import LinkWithF

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


# Create your tests here.
class LinkWithFTests(TestCase):

    def test_code_has_already_expired(self):
        """
            Test case for check_timeout() which returns False for codes that
            had already expired
            INPUT
                - Self
            OUTPUT
                - A boolean value indicating if the test has already passed
        """
        time = timezone.now() + datetime.timedelta(days=-7)
        passed_link_code = LinkWithF(date_of_creation=time)
        self.assertIs(passed_link_code.check_timeout(), False)

class LinkCodeTest(TestCase):

    def test_user_creates_random_code(self):
        """
            The user is going to get a random link code whenever it makes a post
            to the same page.
        """
        user = create_user_provider()
        self.client.login(username="uname", password="testpasswd123")
        response = self.client.post('/provider/my_clients/link_code/')
        print(response.context['code'])
        self.assertNotEqual(response.context['code'], '')
