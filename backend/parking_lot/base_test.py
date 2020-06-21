import pytz

from datetime import datetime, timedelta

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone

from api.models import Slot, Reservation


class BaseTestCase(TestCase):
    @staticmethod
    def get_date_time_for_test(days=0, hours=0, with_timezone=True):
        timedelta_kwargs = dict()

        if days:
            timedelta_kwargs['days'] = days

        if hours:
            timedelta_kwargs['hours'] = hours

        now_datetime = timezone.localtime(timezone.now())
        now_datetime += timedelta(days=10)
        now_datetime = now_datetime.replace().replace(hour=7, minute=0, second=0, microsecond=0)

        now_datetime += timedelta(days=days, hours=hours)

        if not with_timezone:
            return now_datetime.strftime('%Y-%m-%d %H:%M:%S')

        return now_datetime.strftime('%Y-%m-%d %H:%M:%S%z')

    @staticmethod
    def get_normal_user_data():
        return {
            'email': 'test@test.com',
            'password': 'testTest'
        }

    @staticmethod
    def get_super_user_data():
        return {
            'email': 'admin@admin.com',
            'password': 'adminAdmin'
        }

    def create_user(self, user_data):
        if get_user_model().objects.filter(email=user_data['email']).exists():
            return

        self.client.post(
            reverse('user:register'),
            data=user_data
        )

    def create_normal_user(self):
        self.create_user(self.get_normal_user_data())

    def create_super_user(self):
        user_data = self.get_super_user_data()

        self.create_user(user_data)

        get_user_model().objects.filter(email=user_data['email']).update(is_superuser=True)

    def get_normal_user_id(self):
        self.create_normal_user()
        return get_user_model().objects.get(is_superuser=False).id

    def get_super_user_id(self):
        self.create_super_user()
        return get_user_model().objects.get(is_superuser=True).id

    def get_tokens(self, user_data):
        response = self.client.post(
            reverse('user:login'),
            data=user_data
        )

        return response.data['refresh'], response.data['access']

    def get_normal_user_tokens(self):
        return self.get_tokens(self.get_normal_user_data())

    def get_super_user_tokens(self):
        return self.get_tokens(self.get_super_user_data())

    @staticmethod
    def get_headers_dict(access_token):
        return {
            'HTTP_AUTHORIZATION': f'Bearer {access_token}'
        }

    def get_normal_user_headers_dict(self):
        self.create_normal_user()
        refresh_token, access_token = self.get_tokens(self.get_normal_user_data())

        return self.get_headers_dict(access_token)

    def get_super_user_headers_dict(self):
        self.create_super_user()
        refresh_token, access_token = self.get_tokens(self.get_super_user_data())

        return self.get_headers_dict(access_token)

    def create_slot(self, slot_data):
        self.client.post(reverse('api:slots'),
                         data=slot_data,
                         **self.get_super_user_headers_dict())

    @staticmethod
    def create_multiple_slots():
        slots_list = list()

        for coords in range(1, 9):
            for floor in range(1, 2):
                for number in range(1, 5):
                    slots_list.append(Slot(
                        number=number,
                        floor=floor,
                        coords=coords
                    ))

        Slot.objects.bulk_create(slots_list)

    def get_slot_id(self, create=True):
        if create:
            self.create_multiple_slots()

        return Slot.objects.filter(reservations__isnull=True, deleted_at__isnull=True).first().id

    def create_reservation(self, data):
        self.client.post(reverse('api:reservations'),
                         data=data,
                         **self.get_super_user_headers_dict())

    def create_reservation_for_user(self, user_id):
        slot_id = self.get_slot_id()

        reservation_data = {
            'slot': slot_id,
            'user': user_id,
            'reserved_from': self.get_date_time_for_test(),
            'reserved_to': self.get_date_time_for_test(hours=12)
        }

        self.create_reservation(reservation_data)

        reservation_id = Reservation.objects.get(
            slot_id=reservation_data['slot']
        ).id

        return reservation_id

    def create_reservation_for_normal_user(self):
        self.create_normal_user()
        user_id = self.get_normal_user_id()

        return self.create_reservation_for_user(user_id)

    def create_reservation_for_super_user(self):
        self.create_super_user()
        user_id = self.get_super_user_id()

        return self.create_reservation_for_user(user_id)

    def create_reservations_by_user_id(self, user_id):
        reservations_list = list()
        for i in range(0, 30):
            reservations_list.append(Reservation(
                user_id=user_id,
                slot_id=self.get_slot_id(create=False),
                reserved_from=self.get_date_time_for_test(days=i),
                reserved_to=self.get_date_time_for_test(days=i, hours=12)
            ))

        Reservation.objects.bulk_create(reservations_list)

    def create_multiple_reservations_for_super_user(self):
        user_id = self.get_super_user_id()
        self.create_reservations_by_user_id(user_id)

    def create_multiple_reservations_for_normal_user(self):
        user_id = self.get_normal_user_id()
        self.create_reservations_by_user_id(user_id)

    def create_multiple_reservations(self):
        self.create_super_user()
        self.create_normal_user()
        self.create_multiple_slots()

        self.create_multiple_reservations_for_super_user()
        self.create_multiple_reservations_for_normal_user()

    @staticmethod
    def parse_datetime(date_time):
        return datetime.strptime(date_time,
                                 '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S%z')

    def parse_datetime_range(self, reserved_from, reserved_to):
        return self.parse_datetime(reserved_from), self.parse_datetime(reserved_to)
