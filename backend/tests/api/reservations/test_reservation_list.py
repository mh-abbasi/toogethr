from django.urls import reverse

from rest_framework import status

from api.models import Slot, Reservation
from parking_lot.base_test import BaseTestCase


class ReservationListTestCase(BaseTestCase):
    @staticmethod
    def get_url():
        return reverse('api:reservations')

    def test_endpoint_exist(self):
        url = self.get_url()

        self.assertIsNotNone(url)

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_limits_results_by_user(self):
        self.create_multiple_reservations()

        url = self.get_url()
        response = self.client.get(url,
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.data['count'], Reservation.objects.filter(user__is_superuser=False).count())

    def test_endpoint_lists_all_reservations_for_super_user(self):
        self.create_multiple_reservations()

        url = self.get_url()
        response = self.client.get(url,
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.data['count'], Reservation.objects.count())

    def test_endpoint_filters_by_user(self):
        self.create_multiple_reservations()

        user_id = self.get_normal_user_id()

        url = self.get_url()
        response = self.client.get(url,
                                   data={
                                       'user_id': user_id
                                   },
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.data['count'], Reservation.objects.filter(user_id=user_id).count())

    def test_endpoint_filters_by_slot(self):
        self.create_multiple_reservations()

        slot_id = Slot.objects.filter(reservations__isnull=False).first().id

        url = self.get_url()
        response = self.client.get(url,
                                   data={
                                       'slot_id': slot_id
                                   },
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.data['count'], Reservation.objects.filter(slot_id=slot_id).count())

    def test_endpoint_filters_by_date_range(self):
        self.create_multiple_reservations()

        from_date_string = self.get_date_time_for_test(days=10, hours=5, with_timezone=False)
        to_date_string = self.get_date_time_for_test(days=20, hours=5, with_timezone=False)

        url = self.get_url()
        response = self.client.get(url,
                                   data={
                                       'from_date': from_date_string,
                                       'to_date': to_date_string,
                                   },
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

        self.assertEqual(response.data['count'], Reservation.objects.filter(
            reserved_from__gte=self.get_date_time_for_test(days=10, hours=5),
            reserved_to__lte=self.get_date_time_for_test(days=20, hours=5),
        ).count())
