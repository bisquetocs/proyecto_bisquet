from django.test import TestCase, Client
from django.contrib.auth.models import User

import datetime

# Create your tests here.

class LogInOutTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.my_admin = User(username='user', is_staff=True)
        self.my_admin.set_password('password')
        self.my_admin.save() # needed to save to temporary test db
    def testLogIn(self):
        response = self.client.get('/accounts/login/', follow=True)
        loginresponse = self.client.login(username='user',password='password')
        self.assertTrue(loginresponse) # should now return "true"
    def testLogOut(self):
        self.client = Client()
        self.client.login(username='user', password='password')
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)
