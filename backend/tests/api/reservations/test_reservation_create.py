from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class ReservationCreateTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('api:reservations')

    def test_endpoint_exist(self):
        url = self.get_url()

        self.assertIsNotNone(url)

        response = self.client.post(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_validates(self):
        url = self.get_url()

        response = self.client.post(url,
                                    **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('slot', response.data['errors']['fields'])
        self.assertIn('reserved_from', response.data['errors']['fields'])
        self.assertIn('reserved_to', response.data['errors']['fields'])

    def test_endpoint_creates(self):
        slot_id = self.get_slot_id()

        data = {
            'slot': slot_id,
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(hours=12),
        }

        url = self.get_url()
        response = self.client.post(url,
                                    data=data,
                                    **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('slot_data', response.data)
        self.assertIn('user_data', response.data)
        self.assertIn('plate_number', response.data)
        self.assertIn('reserved_from', response.data)
        self.assertIn('reserved_to', response.data)

    def test_endpoint_creates_with_optional_fields(self):
        slot_id = self.get_slot_id()

        data = {
            'slot': slot_id,
            'plate_number': '123qwe123q',
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(hours=12),
        }

        url = self.get_url()
        response = self.client.post(url,
                                    data=data,
                                    **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('slot_data', response.data)
        self.assertIn('user_data', response.data)
        self.assertIn('plate_number', response.data)
        self.assertIn('reserved_from', response.data)
        self.assertIn('reserved_to', response.data)

    def test_cant_create_reservation_in_past(self):
        slot_id = self.get_slot_id()

        data = {
            'slot': slot_id,
            'plate_number': '123qwe123q',
            'reserved_from': self.get_date_time_for_test(days=-20),
            'reserved_to': self.get_date_time_for_test(days=-10),
        }

        url = self.get_url()
        response = self.client.post(url,
                                    data=data,
                                    **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('reserved_from', response.data['errors']['fields'])
        self.assertIn('reserved_to', response.data['errors']['fields'])
