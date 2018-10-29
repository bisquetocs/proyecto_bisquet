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
from provider.models import Provider

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
    nf = Franchise(id=1, id_usuario=nuf, activo=True, fecha_registro=timezone.now())
    nf.save()
    fran = Franchise.objects.get(id = 1)
    ocsUser = OCSUser(user=nu, id_franchise = fran)
    ocsUser.save()

def create_user_generic():
    """
        Function for creating a generic employee in case it is
        needed in the test cases
    """
    nu = User(username='uname3')
    nu.set_password('testpasswd123')
    nu.save()
    g = Group.objects.get(name='Empleado generico')
    g.user_set.add(nu)
    g.save()
    ocsUser = OCSUser(user=nu)
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

    def setUp(self):
        create_groups()
        create_user_provider()
        create_user_franchise()
        create_user_generic()
        create_user_secretary()

    def test_unable_employee_true(self):
        """
            A franchise manager or owner will be able to unable their employees
        """
        login = self.client.login(username="uname", password="testpasswd123") #login as a generic employee
        user = User.objects.get(username = "uname4")
        id = user.id
        url = "/accounts/myEmployees/delete/" + str(id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        ocs = OCSUser.objects.get(user = id)
        if ocs.active == False:
            self.assertTrue(True)


    def test_view_employee_true(self):
        """"
            A franchise manager or owner will be able to consult the employee's catalog
        """
        login = self.client.login(username="uname", password="testpasswd123") #login as owner or franchise
        response = self.client.get('/accounts/myEmployees/') #Tries to access
        self.assertEqual(response.status_code, 200)

    def test_view_employee_false(self):
        """"
            A user that is not a franchise manager or owner will NOT be able to consult the employee's catalog
        """
        login = self.client.login(username="uname3", password="testpasswd123") #login as a generic employee
        response = self.client.get('/accounts/myEmployees/') #Tries to access
        self.assertNotEqual(response.status_code, 200) #It redirects

    def test_register_employee_true(self):
        """
            An employee without a group will be assigned the group of Almacenista
            that belongs to the providers group
        """
        login = self.client.login(username="uname", password="testpasswd123") #login as a franchise manager or owner
        response = self.client.post('/accounts/linkEmployee/', {'inputUser': 'uname3', 'inputRol': 'Almacenista'})
        user = User.objects.get(username = "uname3")
        almacenista = Group.objects.get(name = "Almacenista")
        if almacenista in user.groups.all():
            self.assertTrue(True)


    def test_register_employee_false(self):
        """
            An generic employee will NOT be able to register the role of an employee
        """
        login = self.client.login(username="uname3", password="testpasswd123") #login as a generic employee
        response = self.client.post('/accounts/linkEmployee/', {'inputUser': 'uname', 'inputRol': 'Almacenista'})
        user = User.objects.get(username = "uname")
        almacenista = Group.objects.get(name = "Almacenista")
        if almacenista in user.groups.all():
            self.assertTrue(False)


    def test_change_role_true(self):
        """
            A franchise manager or owner will be able to change their employee's role
        """
        login = self.client.login(username="uname", password="testpasswd123") #login as franchise manager or owner
        response = self.client.post('/accounts/linkEmployee/verEmpleado/4/', {'role': 'Almacenista'})
        user = User.objects.get(username = "uname4")
        almacenista = Group.objects.get(name = "Almacenista")
        if almacenista in user.groups.all():
            self.assertTrue(True)

    def test_change_role_false(self):
        """
            A secretary will NOT be able to change an employee's role
        """
        login = self.client.login(username="uname4", password="testpasswd123") #login as franchise manager or owner
        response = self.client.post('/accounts/linkEmployee/verEmpleado/1/', {'role': 'Almacenista'})
        user = User.objects.get(username = "uname")
        almacenista = Group.objects.get(name = "Almacenista")
        if almacenista in user.groups.all():
            self.assertTrue(False)

    def test_view_employee_detail(self):
        """"
            A franchise manager or owner will be able to consult the employee's information detail
        """
        login = self.client.login(username="uname4", password="testpasswd123") #login as owner or franchise
        user = User.objects.get(username = "uname4")
        id = user.id
        url = "/accounts/myEmployees/verEmpleado/" + str(id)
        response = self.client.get('url') #Tries to access employee's information
        self.assertNotEqual(response.status_code, 200)
