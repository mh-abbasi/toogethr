from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class ReservationUpdateTestCase(BaseTestCase):
    @staticmethod
    def get_url(reservation_id):
        return reverse('api:reservations_item', args=(reservation_id,))

    def test_endpoint_exist(self):
        url = self.get_url(1)

        self.assertIsNotNone(url)

        response = self.client.put(url)

        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_checks_existence_of_reservation(self):
        url = self.get_url(1)

        response = self.client.put(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_endpoint_validates_payload(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'slot': 'fake-id',
            'user': 'fake-id',
            'reserved_from': 'date-time-string',
            'reserved_to': 'date-time-string',
        }

        url = self.get_url(reservation_id)
        response = self.client.put(url,
                                   data=data,
                                   content_type='application/json',
                                   **self.get_normal_user_headers_dict())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('slot', response.data['errors']['fields'])
        self.assertIn('user', response.data['errors']['fields'])
        self.assertIn('reserved_from', response.data['errors']['fields'])
        self.assertIn('reserved_to', response.data['errors']['fields'])

    def test_endpoint_works(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'slot': self.get_slot_id(),
            'reserved_from': self.get_date_time_for_test(days=30, hours=1),
            'reserved_to': self.get_date_time_for_test(days=40, hours=1),
        }

        url = self.get_url(reservation_id)
        response = self.client.put(url,
                                   data=data,
                                   content_type='application/json',
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['slot_data']['id'], data['slot'])

        reserved_from, reserved_to = self.parse_datetime_range(response.data['reserved_from'],
                                                               response.data['reserved_to'])

        self.assertEqual(reserved_from, data['reserved_from'])
        self.assertEqual(reserved_to, data['reserved_to'])

    def test_super_user_can_edit_another_user_reservation(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'slot': self.get_slot_id(),
            'reserved_from': self.get_date_time_for_test(days=30, hours=1),
            'reserved_to': self.get_date_time_for_test(days=40, hours=1)
        }

        url = self.get_url(reservation_id)
        response = self.client.put(url,
                                   data=data,
                                   content_type='application/json',
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['slot_data']['id'], data['slot'])

        reserved_from, reserved_to = self.parse_datetime_range(response.data['reserved_from'],
                                                               response.data['reserved_to'])

        self.assertEqual(reserved_from, data['reserved_from'])
        self.assertEqual(reserved_to, data['reserved_to'])
