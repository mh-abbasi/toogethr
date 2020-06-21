import json
import base64

from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class UserLoginTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('user:login')

    def test_endpoint_exist(self):
        url = self.get_url()

        self.assertIsNotNone(url)

        response = self.client.post(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_login_validate_inputs(self):
        url = self.get_url()

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['errors']['fields'])
        self.assertIn('password', response.data['errors']['fields'])

    def test_login_check_password(self):
        self.create_normal_user()

        user_data = self.get_normal_user_data()
        user_data['password'] = 'Wrong_Password'

        url = self.get_url()

        response = self.client.post(url, data=user_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_works(self):
        self.create_normal_user()

        user_data = self.get_normal_user_data()

        url = self.get_url()

        response = self.client.post(url, data=user_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_token_contains_superuser_parameter(self):
        self.create_super_user()

        user_data = self.get_super_user_data()

        url = self.get_url()
        response = self.client.post(url, data=user_data)

        payload_part = response.data['access'].split('.')[1]
        payload_part = payload_part + ('=' * (4 - (len(payload_part) % 4)))

        payload = json.loads(str(base64.b64decode(payload_part), encoding='UTF-8'))

        self.assertIn('is_superuser', payload)
        self.assertTrue(payload['is_superuser'])
