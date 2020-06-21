from unittest import TestCase

from api.models import Reservation
from parking_lot.base_test import BaseTestCase


class ReservationModelTestCase(BaseTestCase):
    def test_instance_string_with_number(self):
        self.create_reservation_for_normal_user()
        reservation = Reservation.objects.get()

        self.assertEqual(str(reservation), f"{reservation.slot} reserved by {reservation.user}")
