import datetime
from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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

class UserLoginTest(TestCase):

    def test_user_logged_with_incorrect_user_pass(self):
        """
            The user wont be able to login to the system in case the user inserts
            a wrong username or password
        """
        user = create_user_provider()
        test1 = self.client.login(username="WRONG", password="testpasswd123")
        test2 = self.client.login(username="uname", password="WRONG")
        test3 = self.client.login(username="WRONG", password="WRONG")

        result = (test1 or test2 or test3)

        self.assertIs(result, False)

    def test_user_tries_to_enter_home_without_logged_in(self):
        """
            The user will be redirected to the login form in case the user tries to
            access a url that requires a login at the beggining
        """
        user = create_user_provider()
        self.client.login(username="WRONG", password="testpasswd123")
        response = self.client.get('/provider/home/')

        self.assertRedirects(response, '/accounts/login/?next=/provider/home/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
