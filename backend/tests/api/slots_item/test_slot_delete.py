from django.urls import reverse

from rest_framework import status

from api.models import Slot, Reservation
from parking_lot.base_test import BaseTestCase


class SlotDeleteTestCase(BaseTestCase):
    @staticmethod
    def get_url(slot_id):
        return reverse('api:slots_item', args=(slot_id,))

    def test_endpoint_exist(self):
        url = self.get_url(1)

        self.assertIsNotNone(url)

        response = self.client.delete(url)

        self.assertNotEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_endpoint_checks_slot_existence(self):
        url = self.get_url(1)

        response = self.client.delete(url,
                                      **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_endpoint_deletes_slot(self):
        slot_data = {
            'number': 1
        }

        self.create_slot(slot_data)

        slot_id = Slot.objects.get(number=slot_data['number']).id

        url = self.get_url(slot_id)

        response = self.client.delete(url,
                                      **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        slot_queryset = Slot.objects.filter(id=slot_id)
        self.assertTrue(slot_queryset.exists())

        slot = slot_queryset.get()
        self.assertIsNotNone(slot.deleted_at)

    def delete_slot(self):
        slot_data = {
            'number': 1
        }

        self.create_slot(slot_data)

        slot_id = Slot.objects.get(number=slot_data['number']).id

        url = self.get_url(slot_id)

        self.client.delete(url, **self.get_super_user_headers_dict())

        return slot_id

    def test_deleted_slot_appear_for_normal_user_in_list(self):
        self.delete_slot()

        response = self.client.get(reverse('api:slots'),
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_deleted_slot_appear_for_normal_user_in_get(self):
        slot_id = self.delete_slot()

        response = self.client.get(self.get_url(slot_id),
                                   **self.get_normal_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_deleted_slot_appear_for_super_user_in_list(self):
        self.delete_slot()

        response = self.client.get(reverse('api:slots'),
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_deleted_slot_appear_for_super_user_in_get(self):
        slot_id = self.delete_slot()

        response = self.client.get(self.get_url(slot_id),
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deleted_slot_for_update(self):
        slot_id = self.delete_slot()

        response = self.client.get(self.get_url(slot_id),
                                   **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_works_with_number_of_deleted_slot(self):
        slot_id = self.delete_slot()

        number = Slot.objects.get(id=slot_id).number

        response = self.client.post(reverse('api:slots'),
                                    data={
                                        'number': number
                                    },
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_deletion_of_slot_deletes_reservations(self):
        slot_data = {
            'number': 1
        }
        self.create_slot(slot_data)

        slot = Slot.objects.get(number=slot_data['number'])
        slot_id = slot.id
        self.create_reservation({
            'slot': slot_id,
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(hours=12),
        })

        url = self.get_url(slot_id)
        self.client.delete(url, **self.get_super_user_headers_dict())

        self.assertEqual(Reservation.objects.filter(slot_id=slot_id, deleted_at__isnull=True).count(), 0)

    def test_cant_create_reservation_with_delete_slot(self):
        slot_id = self.delete_slot()

        response = self.client.post(reverse('api:reservations'),
                                    data={
                                        'slot': slot_id,
                                        'reserved_from': self.get_date_time_for_test(),
                                        'reserved_to': self.get_date_time_for_test(hours=12),
                                    },
                                    **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cant_update_reservation_to_delete_slot(self):
        slot_id = self.delete_slot()
        reservation_id = self.create_reservation_for_super_user()

        response = self.client.patch(reverse('api:reservations_item', args=(reservation_id,)),
                                     data={
                                         'slot': slot_id
                                     },
                                     content_type='application/json',
                                     **self.get_super_user_headers_dict())

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
