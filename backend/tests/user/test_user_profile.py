from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class UserProfileTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('user:profile')

    def test_endpoint_exist(self):
        url = self.get_url()

        self.assertIsNotNone(url)

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_profile_authenticates(self):
        url = self.get_url()

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_checks_token(self):
        url = self.get_url()

        response = self.client.get(url,
                                   **self.get_headers_dict('fake.token.test'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_works(self):
        url = self.get_url()

        response = self.client.get(url,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('id', response.data)
        self.assertIn('email', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('is_superuser', response.data)
        self.assertNotIn('password', response.data)
