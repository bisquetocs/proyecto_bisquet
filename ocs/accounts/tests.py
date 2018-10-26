import datetime
from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from franchise.models import Franchise

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
        Function for creating a user in case it is needed
        in the test cases
    """
    ng = Group(name='Dueño de franquicia')
    ng.save()
    nu = User(username='uname2')
    nu.set_password('testpasswd123')
    nu.save()
    g = Group.objects.get(name='Dueño de franquicia')
    g.user_set.add(nu)
    g.save()
    ocsUser = OCSUser(user=nu)
    ocsUser.save()
    nf = Franchise(id=1, id_usuario=nu, activo=True, fecha_registro=timezone.now())
    nf.save()

class UserLoginTest(TestCase):

    def test_provider_logged_with_incorrect_user_pass(self):
        """
            The provider user wont be able to login to the system in case the user inserts
            a wrong username or password
        """
        user = create_user_provider()
        test1 = self.client.login(username="WRONG", password="testpasswd123")
        test2 = self.client.login(username="uname", password="WRONG")
        test3 = self.client.login(username="WRONG", password="WRONG")

        result = (test1 or test2 or test3)

        self.assertIs(result, False)

    def test_provider_tries_to_enter_home_without_logged_in(self):
        """
            The provider user will be redirected to the login form in case the user tries to
            access a url that requires a login at the beggining
        """
        user = create_user_provider()
        self.client.login(username="WRONG", password="testpasswd123")
        response = self.client.get('/provider/home/')

        self.assertRedirects(response, '/accounts/login/?next=/provider/home/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_franchise_logged_with_incorrect_user_pass(self):
        """
            The franchise user wont be able to login to the system in case the user inserts
            a wrong username or password
        """
        user = create_user_franchise()
        test1 = self.client.login(username="WRONG", password="testpasswd123")
        test2 = self.client.login(username="uname2", password="WRONG")
        test3 = self.client.login(username="WRONG", password="WRONG")

        result = (test1 or test2 or test3)

        self.assertIs(result, False)

    def test_franchise_tries_to_enter_home_without_logged_in(self):
        """
            The franchise user will be redirected to the login form in case the user tries to
            access a url that requires a login at the beggining
        """
        user = create_user_franchise()
        self.client.login(username="WRONG", password="testpasswd123")
        response = self.client.get('/franchise/home/')

        self.assertRedirects(response, '/accounts/login/?next=/franchise/home/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)


class UserLogoutTest(TestCase):

    def test_provider_logged_out(self):
        """
            Ther provider user will be redirected to the landing page of the OCS
            system once the user logout from the system. In order to logout,
            the user must be logged in
        """
        user = create_user_provider()
        self.client.login(username="uname", password="testpasswd123")
        response = self.client.get('/accounts/accounts/logout/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_franchise_logged_out(self):
        """
            Ther franchise user will be redirected to the landing page of the OCS
            system once the user logout from the system. In order to logout,
            the user must be logged in
        """
        user = create_user_franchise()
        self.client.login(username="uname", password="testpasswd123")
        response = self.client.get('/accounts/accounts/logout/')
        self.assertRedirects(response, '/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)
