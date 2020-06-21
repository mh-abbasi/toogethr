from django.urls import reverse

from rest_framework import status

from parking_lot.base_test import BaseTestCase


class SlotCreateTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('api:slots')

    def test_endpoint_exist(self):
        url = self.get_url()

        self.assertIsNotNone(url)

        response = self.client.post(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_validates(self):
        url = self.get_url()

        response = self.client.post(url,
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_endpoint_validates_payload(self):
        url = self.get_url()

        slot_data = {
            'number': 'not_valid',
            'floor': 'not_valid',
            'coords': 10  # invalid coords
        }

        response = self.client.post(url,
                                    data=slot_data,
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('number', response.data['errors']['fields'])
        self.assertIn('floor', response.data['errors']['fields'])
        self.assertIn('coords', response.data['errors']['fields'])

    def test_endpoint_works_with_optional_fields(self):
        url = self.get_url()

        slot_data = {
            'number': 1,
            'floor': 1,
            'coords': 1
        }

        response = self.client.post(url,
                                    data=slot_data,
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('id', response.data)
        self.assertEqual(response.data['number'], slot_data['number'])
        self.assertEqual(response.data['floor'], slot_data['floor'])
        self.assertEqual(response.data['coords'], slot_data['coords'])

    def test_endpoint_works_without_optional_fields(self):
        url = self.get_url()

        slot_data = {
            'number': 1
        }

        response = self.client.post(url,
                                    data=slot_data,
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn('id', response.data)
        self.assertEqual(response.data['number'], slot_data['number'])

    def test_endpoint_blocks_used_number(self):
        url = self.get_url()

        slot_data = {
            'number': 1
        }

        self.client.post(url,
                         data=slot_data,
                         **self.get_super_user_headers_dict())

        response = self.client.post(url,
                                    data=slot_data,
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('number', response.data['errors']['fields'])
