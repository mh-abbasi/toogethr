from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class PermissionTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('api:slots')

    def test_permission_blocks_anonymous_users(self):
        url = self.get_url()

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permission_allows_normal_users_for_safe_methods(self):
        url = self.get_url()

        response = self.client.get(url,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_blocks_normal_users_for_unsafe_methods(self):
        url = self.get_url()

        response = self.client.post(url,
                                    **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permission_allows_super_users_for_safe_methods(self):
        url = self.get_url()

        response = self.client.get(url,
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_allows_super_users_for_unsafe_methods(self):
        url = self.get_url()

        response = self.client.post(url,
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
