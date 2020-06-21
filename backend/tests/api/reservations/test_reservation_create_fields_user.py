from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status

from api.models import Slot
from parking_lot.base_test import BaseTestCase


class ReservationCreateFieldsUserTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('api:reservations')

    def test_normal_user_cant_create_for_another_users(self):
        slot_id = self.get_slot_id()

        self.create_super_user()
        user_id = self.get_super_user_id()

        data = {
            'slot': slot_id,
            'user': user_id,
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(hours=12),
        }

        url = self.get_url()
        response = self.client.post(url,
                                    data=data,
                                    **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('user', response.data['errors']['fields'])

    def test_super_user_can_create_for_another_users(self):
        slot_id = self.get_slot_id()

        self.create_normal_user()
        user_id = self.get_normal_user_id()

        data = {
            'slot': slot_id,
            'user': user_id,
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(hours=12),
        }

        url = self.get_url()
        response = self.client.post(url,
                                    data=data,
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
