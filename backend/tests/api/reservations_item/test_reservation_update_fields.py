from django.urls import reverse

from rest_framework import status

from api.models import Reservation
from parking_lot.base_test import BaseTestCase


class ReservationUpdateFieldsTestCase(BaseTestCase):
    @staticmethod
    def get_url(reservation_id):
        return reverse('api:reservations_item', args=(reservation_id,))

    def test_endpoint_validates_date_ranges(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'reserved_from': self.get_date_time_for_test(days=20, hours=2),
            'reserved_to': self.get_date_time_for_test(days=10, hours=2),
        }

        url = self.get_url(reservation_id)
        response = self.client.patch(url,
                                     data=data,
                                     content_type='application/json',
                                     **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('reserved_from', response.data['errors']['fields'])
        self.assertIn('reserved_to', response.data['errors']['fields'])

    def test_can_edit_only_slot(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'slot': self.get_slot_id()
        }

        url = self.get_url(reservation_id)
        response = self.client.patch(url,
                                     data=data,
                                     content_type='application/json',
                                     **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['slot_data']['id'], data['slot'])

    def test_normal_user_cant_edit_user(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'user': self.get_super_user_id()
        }

        url = self.get_url(reservation_id)
        response = self.client.patch(url,
                                     data=data,
                                     content_type='application/json',
                                     **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_super_user_can_edit_only_user(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'user': self.get_super_user_id()
        }

        url = self.get_url(reservation_id)
        response = self.client.patch(url,
                                     data=data,
                                     content_type='application/json',
                                     **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['user_data']['id'], data['user'])

    def test_can_edit_only_reserved_from(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'reserved_from': self.get_date_time_for_test(hours=5)
        }

        url = self.get_url(reservation_id)
        response = self.client.patch(url,
                                     data=data,
                                     content_type='application/json',
                                     **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        parsed_reserved_from = self.parse_datetime(response.data['reserved_from'])
        self.assertEqual(parsed_reserved_from, data['reserved_from'])

    def test_can_edit_only_reserved_to(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'reserved_to': self.get_date_time_for_test(hours=5)
        }

        url = self.get_url(reservation_id)
        response = self.client.patch(url,
                                     data=data,
                                     content_type='application/json',
                                     **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        parsed_reserved_to = self.parse_datetime(response.data['reserved_to'])
        self.assertEqual(parsed_reserved_to, data['reserved_to'])

    def test_can_edit_date_range_with_same_value(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(hours=12)
        }

        url = self.get_url(reservation_id)
        response = self.client.patch(url,
                                     data=data,
                                     content_type='application/json',
                                     **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        parsed_reserved_from, parsed_reserved_to = self.parse_datetime_range(response.data['reserved_from'],
                                                                             response.data['reserved_to'])
        self.assertEqual(parsed_reserved_from, data['reserved_from'])
        self.assertEqual(parsed_reserved_to, data['reserved_to'])

    def test_can_edit_date_range_with_same_value_slot(self):
        reservation_id = self.create_reservation_for_normal_user()

        data = {
            'slot': self.get_slot_id(),
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(hours=12)
        }

        url = self.get_url(reservation_id)
        response = self.client.patch(url,
                                     data=data,
                                     content_type='application/json',
                                     **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        parsed_reserved_from, parsed_reserved_to = self.parse_datetime_range(response.data['reserved_from'],
                                                                             response.data['reserved_to'])
        self.assertEqual(parsed_reserved_from, data['reserved_from'])
        self.assertEqual(parsed_reserved_to, data['reserved_to'])
        self.assertEqual(response.data['slot_data']['id'], data['slot'])

    def test_endpoint_validates_date_range(self):
        normal_user_reservation_id = self.create_reservation_for_normal_user()
        super_user_reservation_id = self.create_reservation_for_super_user()

        normal_user_reservation = Reservation.objects.get(id=normal_user_reservation_id)

        data = {
            'slot': normal_user_reservation.slot_id,
            'reserved_from': normal_user_reservation.reserved_from.strftime('%Y-%m-%d %H:%M:%S%z'),
            'reserved_to': normal_user_reservation.reserved_to.strftime('%Y-%m-%d %H:%M:%S%z')
        }

        url = self.get_url(super_user_reservation_id)
        response = self.client.patch(url,
                                     data=data,
                                     content_type='application/json',
                                     **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('slot', response.data['errors']['fields'])
        self.assertIn('reserved_from', response.data['errors']['fields'])
        self.assertIn('reserved_to', response.data['errors']['fields'])
