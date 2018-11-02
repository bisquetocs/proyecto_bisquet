"""
Description: Tests file for the accounts module
Modified by: Fátima
Modify date: 26-10-18
"""

import datetime
from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from franchise.models import Franchise
from provider.models import Provider
from products.models import Product




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




# ---------------TESTS DE BETO ------------------------ #
class BetoTestProduct(TestCase):
    def test_new_product(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        prov = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_provider=prov)
        myuser.save()
        prov.save()
        ocs_user.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.post('/products/register/', {'nombre': 'Producto Nuevo',
                                                                'descripcion': 'Este es un nuevo producto',
                                                                'codigo': 'pRod',
                                                                'activo': 'on'
                                                             })
        num_results = Product.objects.filter(nombre = "producto nuevo").count()
        if num_results > 0:
            exists = True
        self.assertEqual(exists, True)
        prod = Product.objects.get(nombre = "producto nuevo")
        prod2 = Product(nombre= 'producto nuevo',descripcion= 'Este es un nuevo producto',codigo= 'PROD',activo= True)
        prod3 = Product(nombre= 'Producto Nuevo',descripcion= 'Este es un nuevo Producto',codigo= 'pRod',activo= False)
        self.assertRedirects(response, '/products/myProducts/')
        # asi debe de estar
        self.assertEqual(prod.nombre, prod2.nombre)
        self.assertEqual(prod.descripcion, prod2.descripcion)
        self.assertEqual(prod.codigo, prod2.codigo)
        self.assertEqual(prod.activo, prod2.activo)
        # asi NO debe de estar
        self.assertNotEqual(prod.nombre, prod3.nombre)
        self.assertNotEqual(prod.descripcion, prod3.descripcion)
        self.assertNotEqual(prod.codigo, prod3.codigo)
        self.assertNotEqual(prod.activo, prod3.activo)
        # debe tener el Id de provider al que pertenece
        self.assertEqual(prod.id_provider, prov)
        # en el siguiente post el producto NO se debe de registrarse
        response = self.client.post('/products/register/', {'nombre': 'Producto Nuevo',
                                                            'descripcion': 'Este es un nuevo producto con nombre y codigo igual a uno anterior',
                                                            'codigo': 'pRod',
                                                            'activo': 'on'})
        count = Product.objects.all().count()
        self.assertEqual(count, 1)

    def test_ableUnable_product(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        prov = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_provider=prov)
        myuser.save()
        prov.save()
        ocs_user.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.post('/products/register/', {'nombre': 'Producto Nuevo',
                                                                'descripcion': 'Este es un nuevo producto',
                                                                'codigo': 'pRod',
                                                                'activo': 'on'})
        count = Product.objects.all().count()
        self.assertEqual(count, 1)
        prod = Product.objects.get(nombre = "producto nuevo")
        self.assertEqual(prod.activo, True)
        response = self.client.get('/products/ableUnable/1/')
        prod = Product.objects.get(nombre = "producto nuevo")
        self.assertEqual(prod.activo, True)
        self.assertRedirects(response, '/products/myProducts/')

    def test_edit_product(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        prov = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_provider=prov)
        myuser.save()
        prov.save()
        ocs_user.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response0 = self.client.post('/products/register/', {'nombre': 'Producto Nuevo',
                                                                'descripcion': 'Este es un nuevo producto',
                                                                'codigo': 'pRod',
                                                                'activo': 'on'})
        response1 = self.client.post('/products/register/', {'nombre': 'Producto Nuevo 2',
                                                                'descripcion': 'Este es un nuevo producto 2',
                                                                'codigo': 'pRod2',
                                                                'activo': 'on'})
        self.assertRedirects(response0, '/products/myProducts/')
        self.assertRedirects(response1, '/products/myProducts/')
        count = Product.objects.all().count()
        self.assertEqual(count, 2)
        # se va a editar
        response2 = self.client.post('/products/edit/2/', {'nombre': 'Producto Nuevo EDITADO',
                                                            'descripcion': 'Este es el mismo nuevo producto EDITADO',
                                                            'codigo': 'pRod',
                                                            'activo': 'on'})
        prod = Product.objects.get(nombre = "producto nuevo editado")
        self.assertRedirects(response2, '/products/myProducts/')
        self.assertEqual(prod.descripcion, 'Este es el mismo nuevo producto EDITADO')
        self.assertEqual(prod.nombre, 'Producto nuevo editado')
        self.assertNotEqual(prod.nombre, 'Producto Nuevo EDITADO')
        # no se podra editar
        response3 = self.client.post('/products/edit/2/', {'nombre': 'PRODUCTO NUEVO 2',
                                                            'descripcion': 'Este es el mismo nuevo producto',
                                                            'codigo': 'pRod',
                                                            'activo': 'on'})
        prod = Product.objects.get(codigo = "PROD")
        self.assertEqual(response3.context['edit'], True)
        self.assertNotEqual(prod.nombre, 'Producto nuevo 2')
        self.assertEqual(prod.nombre, 'Producto nuevo editado')
        self.assertEqual(prod.descripcion, 'Este es el mismo nuevo producto EDITADO')
        self.assertNotEqual(prod.descripcion, 'Este es el mismo nuevo producto')

class BetoTestLandignPage(TestCase):
    def test_check_landing_page(self):
        self.client = Client()
        landing_response = self.client.get('')
        self.assertContains(landing_response, "OCS - Order Control System", count=1, status_code=200, msg_prefix='', html=True)
        landing_response1 = self.client.get('/accounts/')
        self.assertContains(landing_response1, "OCS - Order Control System", count=1, status_code=200, msg_prefix='', html=True)
        landing_response2 = self.client.get('/accounts/registerUser/')
        self.assertContains(landing_response2, "OCS - Registro", count=1, status_code=200, msg_prefix='', html=True)

    def if_login_and_lannding_page_then_locate_provider(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        prov = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre de proveedor",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_provider=prov)
        myuser.save()
        prov.save()
        ocs_user.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        # entrar a homepage
        landing_response = self.client.get('')
        self.assertRedirects(landing_response, '/ppppppppp/home/', status_code=200, target_status_code=302, msg_prefix='', fetch_redirect_response=True)
        #contiene el nombre del proveedor en el titulo
        self.assertContains(landing_response, "OCS - nombre proveedor", count=1, status_code=200, msg_prefix='', html=True)

    def if_login_and_lannding_page_then_locate_franchise(self):
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
        # entrar a homepage
        landing_response = self.client.get('')
        self.assertRedirects(landing_response, '/fffffffff/home/', status_code=200, target_status_code=302, msg_prefix='', fetch_redirect_response=True)
        #contiene el nombre de la franquicia en el titulo
        self.assertContains(landing_response, "OCS - nome de franquicia", count=1, status_code=200, msg_prefix='', html=True)

class BetoTestProvider(TestCase):
    def test_new_provider(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        ocs_user = OCSUser.objects.create(user=myuser, active=True)
        group = Group.objects.create(name="Administrador de empresa")
        myuser.save()
        ocs_user.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.post('/provider/register/', {'razon_social': 'razon social',
                                                            'rfc': 'rfc',
                                                            'nombre': 'Proveedor nuevo',
                                                            'domicilio': 'domicilio',
                                                            'mision': 'mision',
                                                            'vision': 'vision'})
        prov = Provider.objects.get(nombre = 'Proveedor nuevo')
        ocs_user = OCSUser.objects.get(user=myuser)
        count = Provider.objects.all().count()
        self.assertEqual(count, 1)
        self.assertEqual(myuser.id, prov.id_usuario.id)
        self.assertEqual(ocs_user.id_franchise, None)
        self.assertEqual(ocs_user.id_provider, prov)
        self.assertRedirects(response, '/accounts/locate/', status_code=302, target_status_code=302, msg_prefix='', fetch_redirect_response=True)

    def test_edit_provider_info(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        prov = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre proveedor",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_provider=prov)
        myuser.save()
        prov.save()
        ocs_user.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        count = Provider.objects.all().count()
        self.assertEqual(count, 1)
        response = self.client.post('/provider/profile/edit/', {'razon_social': 'razon social',
                                                            'rfc': 'rfc',
                                                            'nombre': 'Proveedor nuevo EDITADO',
                                                            'domicilio': 'domicilio',
                                                            'mision': 'mision EDITADA',
                                                            'vision': 'vision'})
        count = Provider.objects.all().count()
        self.assertEqual(count, 1)
        prov = Provider.objects.get(nombre = 'Proveedor nuevo EDITADO')
        self.assertNotEqual(prov, None)
        self.assertEqual(prov.mision, 'mision EDITADA')
        self.assertRedirects(response, '/provider/profile/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class BetoTestFranchise(TestCase):
    def test_new_franchise(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        ocs_user = OCSUser.objects.create(user=myuser, active=True)
        group = Group.objects.create(name="Dueño de franquicia")
        myuser.save()
        ocs_user.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.post('/franchise/register/', {'razon_social': 'razon social',
                                                            'rfc': 'rfc',
                                                            'nombre': 'Franquicia nueva',
                                                            'domicilio': 'domicilio'})
        fran = Franchise.objects.get(nombre = 'Franquicia nueva')
        ocs_user = OCSUser.objects.get(user=myuser)
        count = Franchise.objects.all().count()
        self.assertEqual(count, 1)
        self.assertEqual(myuser.id, fran.id_usuario.id)
        self.assertEqual(ocs_user.id_provider, None)
        self.assertEqual(ocs_user.id_franchise, fran)
        self.assertRedirects(response, '/accounts/locate/', status_code=302, target_status_code=302, msg_prefix='', fetch_redirect_response=True)

    def test_edit_franchise_info(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        fran = Franchise.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre proveedor",
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
        count = Franchise.objects.all().count()
        self.assertEqual(count, 1)
        response = self.client.post('/franchise/profile/edit/', {'razon_social': 'razon social',
                                                            'rfc': 'rfc',
                                                            'nombre': 'Franquicia nueva EDITADA',
                                                            'domicilio': 'domicilio EDITADO'})
        count = Franchise.objects.all().count()
        self.assertEqual(count, 1)
        fran = Franchise.objects.get(nombre = 'Franquicia nueva EDITADA')
        self.assertNotEqual(fran, None)
        self.assertEqual(fran.domicilio, 'domicilio EDITADO')
        self.assertRedirects(response, '/franchise/profile/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class BetoTestAccounts(TestCase):
    def test_edit_personal_info_provider(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        prov = Provider.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre proveedor",
                                                domicilio= "domicilio",
                                                mision = "Mision",
                                                vision = "Vision",
                                                activo = True,
                                                fecha_registro = timezone.now(),
                                                id_usuario = myuser)
        ocs_user = OCSUser.objects.create(user=myuser, active=True, id_provider=prov)
        myuser.save()
        prov.save()
        ocs_user.save()
        self.client = Client()
        self.client.login(username="user", password="testpassword")
        response = self.client.post('/accounts/profile/edit/', {'first_name': 'Alberto',
                                                            'last_name': 'Martin',
                                                            'email': 'alberttomarvel@gmail.com',
                                                            'phone': '4422822317',
                                                            'domicilio': 'mi domicilio',
                                                            'num_ss': 'numero de ss',
                                                            'rfc':'rfc'})
        myuser = User.objects.get(email='alberttomarvel@gmail.com')
        ocs_user = OCSUser.objects.get(user = myuser)
        self.assertNotEqual(ocs_user, None)
        self.assertEqual(myuser.first_name, 'Alberto')
        self.assertEqual(myuser.last_name, 'Martin')
        self.assertEqual(ocs_user.direccion, 'mi domicilio')
        self.assertEqual(ocs_user.phone, '4422822317')
        self.assertRedirects(response, '/accounts/profile/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)

    def test_edit_personal_info_franchise(self):
        myuser = User.objects.create_user(username="user",email="exampleone@example.com",password="testpassword")
        fran = Franchise.objects.create(razon_social="Razon social",
                                                rfc= "rfc",
                                                nombre= "nombre proveedor",
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
        response = self.client.post('/accounts/profile/edit/', {'first_name': 'Alberto',
                                                            'last_name': 'Martin',
                                                            'email': 'alberttomarvel@gmail.com',
                                                            'phone': '4422822317',
                                                            'domicilio': 'mi domicilio',
                                                            'num_ss': 'numero de ss',
                                                            'rfc':'rfc'})
        myuser = User.objects.get(email='alberttomarvel@gmail.com')
        ocs_user = OCSUser.objects.get(user = myuser)
        self.assertNotEqual(ocs_user, None)
        self.assertEqual(myuser.first_name, 'Alberto')
        self.assertEqual(myuser.last_name, 'Martin')
        self.assertEqual(ocs_user.direccion, 'mi domicilio')
        self.assertEqual(ocs_user.phone, '4422822317')
        self.assertRedirects(response, '/accounts/profile/', status_code=302, target_status_code=200, msg_prefix='', fetch_redirect_response=True)




#
