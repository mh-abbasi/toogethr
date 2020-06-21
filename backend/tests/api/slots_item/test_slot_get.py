from django.urls import reverse

from rest_framework import status

from api.models import Slot
from parking_lot.base_test import BaseTestCase


class SlotGetTestCase(BaseTestCase):
    @staticmethod
    def get_url(slot_id):
        return reverse('api:slots_item', args=(slot_id,))

    def test_endpoint_exist(self):
        url = self.get_url(1)

        self.assertIsNotNone(url)

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_checks_slot_existence(self):
        url = self.get_url(1)

        response = self.client.get(url,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_endpoint_retrieves_slot(self):
        slot_data = {
            'number': 1
        }

        self.create_slot(slot_data)

        slot_id = Slot.objects.get(number=slot_data['number']).id

        url = self.get_url(slot_id)

        response = self.client.get(url,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
