import json
import bcrypt

from .models import User
from django.test import TestCase
from django.test import Client
from unittest.mock import patch, MagicMock

class SignUpViewTest(TestCase):
    def setUp(self):
        User.objects.create(
            first_name = 'sooji',
            last_name = 'Hwang',
            birthday = '1992-05-04',
            email = 'ifyouseeksooji@gmail.com',
            password = '54321'
        )

        User.objects.create(
            first_name = 'jimin',
            last_name = 'Shin',
            birthday = '2000-03-02',
            email = 'ifyouseekjimin@gmail.com',
            password = '56789'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signup_post_success(self):
        client = Client()
        user = {
            'first_name' : 'nara',
            'last_name' : 'Kim',
            'birthday' : '1989-07-08',
            'email' : 'ninitita@gmail.com',
            'password' : '13579'
        }
        response = client.post('/user/signup', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)
            
            

# Create your tests here.
