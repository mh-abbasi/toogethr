from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status


class UserRegisterTestCase(TestCase):
    @staticmethod
    def get_url():
        return reverse('user:register')

    def test_endpoint_exist(self):
        url = self.get_url()

        self.assertIsNotNone(url)

        response = self.client.post(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_register_validate_inputs(self):
        url = self.get_url()

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['errors']['fields'])
        self.assertIn('password', response.data['errors']['fields'])

    def test_register_works(self):
        url = self.get_url()

        user_data = {
            'email': 'test@test.com',
            'password': 'test'
        }

        response = self.client.post(url, data=user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_validates_for_registered_email(self):
        url = self.get_url()

        user_data = {
            'email': 'test@test.com',
            'password': 'test'
        }

        self.client.post(url, data=user_data)
        response = self.client.post(url, data=user_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['errors']['fields'])

    def test_register_works_with_optional_fields(self):
        url = self.get_url()

        user_data = {
            'email': 'test@test.com',
            'password': 'test',
            'first_name': 'John',
            'last_name': 'Doe',
        }

        response = self.client.post(url, data=user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=user_data['email'])

        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])
