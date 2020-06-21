from django.urls import reverse

from rest_framework import status

from api.models import Slot
from parking_lot.base_test import BaseTestCase


class SlotUpdateTestCase(BaseTestCase):
    @staticmethod
    def get_url(slot_id):
        return reverse('api:slots_item', args=(slot_id,))

    def test_endpoint_exist(self):
        url = self.get_url(1)

        self.assertIsNotNone(url)

        response = self.client.put(url)

        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_checks_slot_existence(self):
        url = self.get_url(1)

        response = self.client.put(url,
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_endpoint_validates_payload(self):
        slot_data = {
            'number': 1
        }

        self.create_slot(slot_data)

        slot_id = Slot.objects.get(number=slot_data['number']).id

        url = self.get_url(slot_id)

        slot_new_data = {
            'number': 'asd',
            'floor': 'asd',
            'coords': 11
        }

        response = self.client.put(url,
                                   data=slot_new_data,
                                   content_type='application/json',
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('number', response.data['errors']['fields'])
        self.assertIn('floor', response.data['errors']['fields'])
        self.assertIn('coords', response.data['errors']['fields'])

    def test_endpoint_updates_slot(self):
        slot_data = {
            'number': 1
        }

        self.create_slot(slot_data)

        slot_id = Slot.objects.get(number=slot_data['number']).id

        url = self.get_url(slot_id)

        slot_new_data = {
            'number': 2,
            'floor': 1,
            'coords': 1
        }

        response = self.client.put(url,
                                   data=slot_new_data,
                                   content_type='application/json',
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['number'], slot_new_data['number'])
        self.assertEqual(response.data['floor'], slot_new_data['floor'])
        self.assertEqual(response.data['coords'], slot_new_data['coords'])
