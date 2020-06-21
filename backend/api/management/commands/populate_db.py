import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from api.models import Slot


class Command(BaseCommand):
    help = 'Run commands to prepare backend for developing'

    def handle(self, *args, **options):
        user_model = get_user_model()

        if not user_model.objects.filter(email='admin@admin.com'):
            user_model.objects.create_user(
                email='admin@admin.com',
                password='admin',
                is_staff=True,
                is_superuser=True,
                first_name='Admin',
                last_name='',
            )

        slot_list = list()
        for number in range(1, 20):
            slot_list.append(Slot(
                number=number,
                floor=random.randint(-3, 3),
                coords=random.randint(1, 9)
            ))

        Slot.objects.bulk_create(slot_list)
