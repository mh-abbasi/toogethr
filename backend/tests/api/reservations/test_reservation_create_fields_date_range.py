from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class ReservationCreateFieldsDateRangeTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('api:reservations')

    def create_test_reservation(self):
        slot_id = self.get_slot_id()

        self.create_normal_user()
        user_id = self.get_normal_user_id()

        data = {
            'slot': slot_id,
            'user': user_id,
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(hours=12),
        }

        self.create_reservation(data)

        return data

    def test_endpoint_validates_date_range(self):
        slot_id = self.get_slot_id()

        self.create_super_user()
        user_id = self.get_super_user_id()

        data = {
            'slot': slot_id,
            'user': user_id,
            'reserved_from': self.get_date_time_for_test(hours=12),
            'reserved_to': self.get_date_time_for_test(),
        }

        url = self.get_url()

        response = self.client.post(url,
                                    data=data,
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('reserved_from', response.data['errors']['fields'])
        self.assertIn('reserved_to', response.data['errors']['fields'])

    def test_endpoint_checks_reservation_dates(self):
        data = self.create_test_reservation()

        self.create_super_user()
        user_id = self.get_super_user_id()

        data['user'] = user_id
        data['reserved_from'] = self.get_date_time_for_test(hours=2)
        data['reserved_to'] = self.get_date_time_for_test(hours=14)

        url = self.get_url()
        response = self.client.post(url,
                                    data=data,
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_endpoint_creates_reservation_on_different_slot_with_same_data(self):
        data = self.create_test_reservation()

        data['slot'] = self.get_slot_id()

        url = self.get_url()
        response = self.client.post(url,
                                    data=data,
                                    **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
