from django.urls import reverse

from rest_framework import status

from api.models import Slot
from parking_lot.base_test import BaseTestCase


class SlotListTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('api:slots')

    def test_empty_filter_checks_existence_of_date_range(self):
        url = self.get_url()
        response = self.client.get(url,
                                   {
                                       'empty': True
                                   },
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('empty', response.data['errors']['fields'])
        self.assertIn('from_datetime', response.data['errors']['fields'])
        self.assertIn('to_datetime', response.data['errors']['fields'])

    def test_empty_filter_works(self):
        self.create_multiple_slots()

        url = self.get_url()
        response = self.client.get(url,
                                   {
                                       'empty': True,
                                       'from_datetime': self.get_date_time_for_test(),
                                       'to_datetime': self.get_date_time_for_test(days=120),
                                   },
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, response.status_code)
        self.assertEqual(response.data['count'], Slot.objects.count())

    def create_reservation_for_filter_test(self):
        normal_user_id = self.get_normal_user_id()
        super_user_id = self.get_super_user_id()

        self.create_reservation({
            'slot': self.get_slot_id(),
            'user': normal_user_id,
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(days=60),
        })

        self.create_reservation({
            'slot': self.get_slot_id(),
            'user': super_user_id,
            'reserved_from': self.get_date_time_for_test(days=30),
            'reserved_to': self.get_date_time_for_test(days=90, hours=1),
        })

    def test_empty_filter_works_with_from_datetime(self):
        self.create_reservation_for_filter_test()

        url = self.get_url()
        response = self.client.get(url,
                                   {
                                       'empty': True,
                                       'from_datetime': self.get_date_time_for_test(days=61),
                                   },
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, response.status_code)
        self.assertEqual(response.data['count'], Slot.objects.count() - 1)

    def test_empty_filter_works_with_to_datetime(self):
        self.create_reservation_for_filter_test()

        url = self.get_url()
        response = self.client.get(url,
                                   {
                                       'empty': True,
                                       'to_datetime': self.get_date_time_for_test(days=1)
                                   },
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, response.status_code)
        self.assertEqual(response.data['count'], Slot.objects.count() - 1)

    def test_empty_filter_works_with_datetime_range(self):
        self.create_reservation_for_filter_test()

        url = self.get_url()
        response = self.client.get(url,
                                   {
                                       'empty': True,
                                       'from_datetime': self.get_date_time_for_test(days=25),
                                       'to_datetime': self.get_date_time_for_test(days=85)
                                   },
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, response.status_code)
        self.assertEqual(response.data['count'], Slot.objects.count() - 2)
