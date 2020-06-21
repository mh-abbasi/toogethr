from django.urls import reverse
from rest_framework import status

from api.models import Reservation
from parking_lot.base_test import BaseTestCase


class ReservationDeleteTestCase(BaseTestCase):
    @staticmethod
    def get_url(reservation_id):
        return reverse('api:reservations_item', args=(reservation_id,))

    def test_endpoint_exist(self):
        url = self.get_url(1)

        self.assertIsNotNone(url)

        response = self.client.delete(url)

        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_checks_reservation_existence(self):
        url = self.get_url(1)

        response = self.client.delete(url,
                                      **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_endpoint_deletes_reservation(self):
        reservation_id = self.create_reservation_for_super_user()

        url = self.get_url(reservation_id)
        response = self.client.delete(url,
                                      **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        reservation_queryset = Reservation.objects.filter(id=reservation_id)
        self.assertTrue(reservation_queryset.exists())

        reservation = reservation_queryset.get()
        self.assertIsNotNone(reservation.deleted_at)

    def test_super_user_can_delete_other_users_reservation(self):
        reservation_id = self.create_reservation_for_normal_user()

        url = self.get_url(reservation_id)
        response = self.client.delete(url,
                                      **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        reservation_queryset = Reservation.objects.filter(id=reservation_id)
        self.assertTrue(reservation_queryset.exists())

        reservation = reservation_queryset.get()
        self.assertIsNotNone(reservation.deleted_at)

    def test_normal_user_can_delete_own_reservation(self):
        reservation_id = self.create_reservation_for_normal_user()

        url = self.get_url(reservation_id)
        response = self.client.delete(url,
                                      **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        reservation_queryset = Reservation.objects.filter(id=reservation_id)
        self.assertTrue(reservation_queryset.exists())

        reservation = reservation_queryset.get()
        self.assertIsNotNone(reservation.deleted_at)

    def test_normal_user_cant_delete_others_reservation(self):
        reservation_id = self.create_reservation_for_super_user()

        url = self.get_url(reservation_id)
        response = self.client.delete(url,
                                      **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        reservation_queryset = Reservation.objects.filter(id=reservation_id)
        self.assertTrue(reservation_queryset.exists())

        reservation = reservation_queryset.get()
        self.assertIsNone(reservation.deleted_at)

    def test_reservation_can_be_created_with_deleted_reservation_data(self):
        reservation_id = self.create_reservation_for_super_user()

        url = self.get_url(reservation_id)
        self.client.delete(url,
                           **self.get_super_user_headers_dict())

        reservation = Reservation.objects.get(id=reservation_id)
        data = {
            'slot': reservation.slot_id,
            'reserved_from': reservation.reserved_from,
            'reserved_to': reservation.reserved_to
        }
        response = self.client.post(reverse('api:reservations'),
                                    data=data,
                                    **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
