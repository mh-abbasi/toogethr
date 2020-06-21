from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class ReservationGetTestCase(BaseTestCase):
    @staticmethod
    def get_url(reservation_id):
        return reverse('api:reservations_item', args=(reservation_id,))

    def test_endpoint_exist(self):
        url = self.get_url(1)

        self.assertIsNotNone(url)

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_checks_reservation_existence(self):
        url = self.get_url(1)

        response = self.client.get(url,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_endpoint_retrieves_reservation(self):
        reservation_id = self.create_reservation_for_normal_user()

        url = self.get_url(reservation_id)

        response = self.client.get(url,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertNotIn('user', response.data)
        self.assertNotIn('slot', response.data)
        self.assertIn('user_data', response.data)
        self.assertIn('slot_data', response.data)
        self.assertIn('reserved_from', response.data)
        self.assertIn('reserved_to', response.data)
        self.assertIn('plate_number', response.data)

    def test_endpoint_limits_normal_user(self):
        reservation_id = self.create_reservation_for_super_user()

        url = self.get_url(reservation_id)

        response = self.client.get(url,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_endpoint_retrieves_other_users_reservation_for_super_user(self):
        reservation_id = self.create_reservation_for_normal_user()

        url = self.get_url(reservation_id)

        response = self.client.get(url,
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
