"""
created by:     Django
Description: Tests file for the providers module
Modified by: Fátima
Modify date: 26-10-18
"""
import datetime
from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from franchise.models import Franchise
from provider.models import Provider, OfficeHours
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import LinkWithF, Days, OfficeHours, DailyClients

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


def create_days():
    """Function used to create day objects"""
    Days.objects.create(nombre = 'Lunes')
    Days.objects.create(nombre = 'Martes')
    Days.objects.create(nombre = 'Miercoles')
    Days.objects.create(nombre = 'Jueves')
    Days.objects.create(nombre = 'Viernes')
    Days.objects.create(nombre = 'Sabado')
    Days.objects.create(nombre = 'Domingo')

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
    nf = Franchise(id=1, nombre = "Franquicia", id_usuario=nuf, activo=True, fecha_registro=timezone.now())
    nf.save()
    fran = Franchise.objects.get(id = 1)
    ocsUser = OCSUser(user=nu, id_franchise = fran)
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

def create_hours():
    prov = Provider.objects.get(id = 1)
    lunes = Days.objects.get(nombre = "Lunes")
    martes = Days.objects.get(nombre = "Martes")
    miercoles = Days.objects.get(nombre = "Miercoles")
    jueves = Days.objects.get(nombre = "Jueves")
    viernes = Days.objects.get(nombre = "Viernes")
    sabado = Days.objects.get(nombre = "Sabado")
    domingo = Days.objects.get(nombre = "Domingo")

    OfficeHours.objects.create(day = lunes, id_provider = prov, start_hour = "7:00", finish_hour = "19:00")
    OfficeHours.objects.create(day = martes, id_provider = prov, start_hour = "7:00", finish_hour = "19:00")
    OfficeHours.objects.create(day = miercoles, id_provider = prov, start_hour = "7:00", finish_hour = "19:00")
    OfficeHours.objects.create(day = jueves, id_provider = prov, start_hour = "7:00", finish_hour = "19:00")
    OfficeHours.objects.create(day = viernes, id_provider = prov, start_hour = "7:00", finish_hour = "19:00")
    OfficeHours.objects.create(day = sabado, id_provider = prov, start_hour = "7:00", finish_hour = "19:00")
    OfficeHours.objects.create(day = domingo, id_provider = prov, start_hour = "7:00", finish_hour = "19:00")


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


class OfficeHoursTest(TestCase):
    def setUp(self):
        create_days()
        create_groups()
        create_user_provider()
        create_user_secretary()
        create_hours()


    def test_view_office_true(self):
        """
            Only the owner will be able to access the assign hours page
        """
        login = self.client.login(username="uname", password="testpasswd123") #login as owner
        response = self.client.get('/provider/office/')
        self.assertEqual(response.status_code, 200)

    def test_view_office_false(self):
        """
            A user who is not owner will NOT be able to access the assign hours page
        """
        login = self.client.login(username="uname4", password="testpasswd123") #login as a Secretary
        response = self.client.get('/provider/office/')
        self.assertNotEqual(response.status_code, 200)


    def test_assign_office_hours(self):
        """
            The owner will be able to assign a start hour and finish hour for each day
        """

        login = self.client.login(username="uname", password="testpasswd123") #login as owner
        response = self.client.post('/provider/office/', {'start_hour_1': '11:00',
                                                            'finish_hour_1': '18:00',
                                                            'start_hour_2': '12:00',
                                                            'finish_hour_2': '18:00',
                                                            'start_hour_3': '12:00',
                                                            'finish_hour_3': '18:00',
                                                            'start_hour_4': '12:00',
                                                            'finish_hour_4': '18:00',
                                                            'start_hour_5': '12:00',
                                                            'finish_hour_5': '18:00',
                                                            'start_hour_6': '12:00',
                                                            'finish_hour_6': '18:00',
                                                            'start_hour_7': '12:00',
                                                            'finish_hour_7': '18:00'})

        self.assertEqual(response.status_code, 200)
        hour = OfficeHours.objects.get(day = 1, id_provider = 1)
        if (hour.start_hour == "12:00" and hour.finish_hour == "18:00"):
            self.assertTrue(True)
        else:
            self.assertTrue(False)


class DailyClientsTest(TestCase):
    def setUp(self):
        create_days()
        create_groups()
        create_user_provider()
        create_user_franchise()
        create_user_secretary()

    def test_view_daily_clients_true(self):
        """
            The owner will be able to consult its daily clients
        """
        login = self.client.login(username="uname", password="testpasswd123") #login as owner
        response = self.client.get("/provider/my_clients/daily_clients")
        self.assertEqual(response.status_code, 200)

    def test_view_daily_clients_false(self):
        """
            A user that is not an owner will NOT be able to consult its daily clients
        """
        login = self.client.login(username="uname4", password="testpasswd123") #login as a secretary
        response = self.client.get("/provider/my_clients/daily_clients")
        self.assertNotEqual(response.status_code, 200)

    def test_assign_daily_clients(self):
        """
            The owner will be able to assign a clients to each of the days of the week
        """
        login = self.client.login(username="uname", password="testpasswd123") #login as owner
        response = self.client.post('/provider/my_clients/daily_clients', {'day':'Lunes', 'client':'Franquicia'})
        self.assertEqual(response.status_code, 200)

    def test_assign_daily_clients_false(self):
        """
            A user that is not an owner will NOT be able to assign a daily clients
        """
        login = self.client.login(username="uname4", password="testpasswd123") #login as a secretary
        response = self.client.post('/provider/my_clients/daily_clients', {'day':'Lunes', 'client':'Franquicia'})
        self.assertNotEqual(response.status_code, 200)
