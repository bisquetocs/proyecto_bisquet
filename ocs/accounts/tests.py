"""
Description: Tests file for the accounts module
Modified by: Fátima
Modify date: 26-10-18
"""

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

def create_group():
    """
        Function for creating a group for a generic employee in case it is
        needed in the test cases
    """
    ng = Group(name='Empleado generico')
    ng.save()


def create_user_generic():
        """
            Function for creating a generic employee in case it is
            needed in the test cases
        """
        ng = Group(name='Empleado generico')
        ng.save()
        nu = User(username='uname3')
        nu.set_password('testpasswd123')
        nu.save()
        g = Group.objects.get(name='Empleado generico')
        g.user_set.add(nu)
        g.save()
        ocsUser = OCSUser(user=nu)
        ocsUser.save()

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

class CreateUserTest(TestCase):

    def test_user_register_new_account(self):
        """
            An unregistered user will be redirected to the landing page of the OCS
            system once the user insert the correct data in the registration form. Also
            a new user will be registered.
        """
        group = create_group()
        response = self.client.post('/accounts/registerUser/', {'first_name': 'contact',
                                                                                'username': 'testuname',
                                                                                'firstName': 'testFirstName',
                                                                                'lastName': 'testLN',
                                                                                'email': 'mail@test.com',
                                                                                'password': 'passTest',
                                                                                'confpass': 'passTest',
                                                                             })

        self.assertRedirects(response, '/accounts/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class EmployeesModuleTest(TestCase):

    def test_employee_provider(self):
        """
            An employee without a group will be assigned the group of Almacenista
            that belongs to the providers group
        """
        employee = create_user_generic()
        group = Group(name='Almacenista')
        response = self.client.post('/accounts/linkEmployee/', {'inputUser': 'uname3', 'inputRol': 'Almacenista'})
        self.assertEqual(response.status_code, 302)

    def test_employee_franchise(self):
        """
            An employee without a group will be assigned the group of Gerente de compras
            that belongs to the franchises group
        """
        employee = create_user_generic()
        group = Group(name='Gerente de compras')
        response = self.client.post('/accounts/linkEmployee/', {'inputUser': 'uname3', 'inputRol': 'Gerente de compras'})
        self.assertEqual(response.status_code, 302)

    def test_view_detail_provider(self):
        """
            A owner will be able to consult its employees information
        """
        user = create_user_provider()
        response = self.client.get('/accounts/myEmployees/verEmpleado/1')
        self.assertNotEqual(response.content, '')

    def test_view_detail_franchise(self):
        """
            A franchise manager will be able to consult its employees information
        """
        user = create_user_franchise()
        response = self.client.get('/accounts/myEmployees/verEmpleado/1')
        self.assertNotEqual(response.content, '')

    def test_view_employee(self):
        """
            A franchise manager or owner will be able to consult its employees catalog
        """
        user = create_user_franchise() #this can be changed to provider
        response = self.client.get('/accounts/myEmployees/')
        self.assertNotEqual(response.content, '')

    def test_unable_employee(self):
        """
            A franchise manager or owner will be able to unable their employees
        """
        user = create_user_provider() #this caan be changed to franchises
        response = self.client.get('/accounts/myEmployees/delete/1/')
        self.assertNotEqual(response.content, '')

    def test_change_role(self):
        """
            A franchise manager or owner will be able to update their employees role
            in the view their employees information detail
        """
        user = create_user_provider() #this can be changed to franchises
        group = Group(name='Almacenista')
        response = self.client.post('/accounts/myEmployees/verEmpleado/1/', {'role': 'Almacenista'})
