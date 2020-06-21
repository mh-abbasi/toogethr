from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.test import TestCase

from api.models import Slot
from parking_lot.base_test import BaseTestCase


class AddDataManagementCommandTestCase(BaseTestCase):
    def test_command_exist(self):
        call_command('populate_db')

    def test_command_creates_superuser(self):
        call_command('populate_db')

        superuser_queryset = get_user_model().objects.filter(is_superuser=True)
        self.assertTrue(superuser_queryset.exists())

    def test_command_works_when_superuser_is_created(self):
        self.create_super_user()
        call_command('populate_db')

        superuser_queryset = get_user_model().objects.filter(is_superuser=True)
        self.assertTrue(superuser_queryset.exists())

    def test_command_creates_slots(self):
        call_command('populate_db')
        slots_queryset = Slot.objects.all()

        self.assertTrue(slots_queryset.exists())
