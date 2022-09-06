import json
import os
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from .models import Owner, SysUser


class RegistrationTestCase(APITestCase):

    def setUp(self):
        self.authorization = os.environ.get('DJANGO_API_KEY')

        self.api_auth()

    def api_auth(self):
        self.client.credentials(HTTP_API_KEY=self.authorization)
    
    def test_registration(self):

        data = {
            'first_name': 'Jon',
            'last_name': 'Snow',
            'username': 'jonsnow3',
            'password': 'AwesomePassword!'
        }

        response = self.client.post('/api/v1/user/config/', data=data)

        self.assertEqual(response.status_code, 200, response.json())


class UserConfigViewSetTestCase(APITestCase):
    def setUp(self):
        self.authorization = os.environ.get('DJANGO_API_KEY')
        self.user = User.objects.create_user(username='jonsnow3', password='AwesomePassword!')
        self.owner = Owner.objects.create(user=self.user)
        self.sys_user = SysUser.objects.create(user=self.user, owner=self.owner)

        self.api_auth()

    def api_auth(self):
        self.client.credentials(HTTP_USERNAME='jonsnow3', HTTP_PASSWORD='AwesomePassword!', HTTP_API_KEY=self.authorization)

    def test_auth_user(self):
        response = self.client.get('/api/v1/user/config/')

        self.assertEqual(response.status_code, 200, response.json())