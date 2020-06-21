import base64
import json

from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class UserRefreshTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('user:refresh')

    def test_endpoint_exist(self):
        url = self.get_url()

        self.assertIsNotNone(url)

        response = self.client.post(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_refresh_validate_inputs(self):
        url = self.get_url()

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('refresh', response.data['errors']['fields'])

    def test_refresh_checks_token(self):
        data = {
            'refresh': 'fake.token.test'
        }

        url = self.get_url()

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_works(self):
        self.create_normal_user()
        refresh_token, access_token = self.get_normal_user_tokens()

        url = self.get_url()

        data = {
            'refresh': refresh_token
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_new_token_contains_superuser_parameter(self):
        self.create_super_user()
        refresh_token, access_token = self.get_super_user_tokens()

        url = self.get_url()

        data = {
            'refresh': refresh_token
        }

        response = self.client.post(url, data=data)

        payload_part = response.data['access'].split('.')[1]
        payload_part = payload_part + ('=' * (4 - (len(payload_part) % 4)))

        payload = json.loads(str(base64.b64decode(payload_part), encoding='UTF-8'))

        self.assertIn('is_superuser', payload)
        self.assertTrue(payload['is_superuser'])
