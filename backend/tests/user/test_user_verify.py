from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class UserVerifyTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('user:verify')

    def test_endpoint_exist(self):
        url = self.get_url()

        self.assertIsNotNone(url)

        response = self.client.post(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_verify_validate_inputs(self):
        url = self.get_url()

        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('token', response.data['errors']['fields'])

    def test_verify_checks_token(self):
        data = {
            'token': 'fake.token.test'
        }

        url = self.get_url()

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_works(self):
        self.create_normal_user()
        refresh_token, access_token = self.get_normal_user_tokens()

        url = self.get_url()

        response = self.client.post(url, data={
            'token': access_token
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
