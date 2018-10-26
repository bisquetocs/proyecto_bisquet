"""
Description: Tests file for the providers module
Modified by: Fátima
Modify date: 26-10-18
"""
import datetime
from django.contrib.auth.models import User, Group
from accounts.models import OCSUser
from franchise.models import Franchise
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import LinkWithF, Days, OfficeHours, DailyClients

def create_days():
    """Function used to create day objects"""
    lunes = Days(nombre = 'Lunes')
    martes = Days(nombre = 'Martes')
    miercoles = Days(nombre = 'Miercoles')
    jueves = Days(nombre = 'Jueves')
    viernes = Days(nombre = 'Viernes')
    sabado = Days(nombre = 'Sabado')
    domingo = Days(nombre = 'Domingo')

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
    nf = Franchise(id=1, nombre = 'Franquicia' ,id_usuario=nu, activo=True, fecha_registro=timezone.now())
    nf.save()

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

    def test_assign_office_hours(self):
        """
            The owner will be able to assign a start hour and finish hour for each day
        """
        days = create_days()
        response = self.client.post('/provider/office/', {'start_hour_1': '12:00',
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

        self.assertEqual(response.status_code, 302)

class DailyClientsTest(TestCase):

    def test_assign_office_hours(self):
        """
            The owner will be able to assign a clients to each of the days of the week
        """
        prev = create_user_provider()
        lunes = Days(nombre = 'Lunes')
        fran = Franchise(id=1, nombre = 'Franquicia' ,id_usuario=nu, activo=True, fecha_registro=timezone.now())

        response = self.client.post('/provider/my_clients/daily_clients/', {'day':'Lunes', 'client':'Franquicia'})
        self.assertEqual(response.status_code, 302)
