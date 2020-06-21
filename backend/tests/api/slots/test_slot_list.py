from django.urls import reverse

from rest_framework import status

from api.models import Slot
from parking_lot.base_test import BaseTestCase


class SlotListTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('api:slots')

    def test_endpoint_exist(self):
        url = self.get_url()

        self.assertIsNotNone(url)

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_works(self):
        self.create_slot({
            'number': 1
        })

        url = self.get_url()

        response = self.client.get(url,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['number'], 1)

    def test_endpoint_filters(self):
        self.create_multiple_slots()

        url = self.get_url()

        filter_data = {
            'number': 3,
            'floor': 7,
            'coords': 2
        }

        response = self.client.get(url, filter_data,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['count'], Slot.objects.filter(**filter_data).count())
