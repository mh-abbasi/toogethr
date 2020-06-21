from unittest import TestCase

from api.models import Slot


class SlotModelTestCase(TestCase):
    def test_instance_string_with_number(self):
        data = {
            'number': 1
        }

        slot = Slot.objects.create(**data)

        self.assertEqual(str(slot), f"{data['number']}")

    def test_instance_string_with_number_and_floor(self):
        data = {
            'number': 1,
            'floor': 1
        }

        slot = Slot.objects.create(**data)

        self.assertEqual(str(slot), f"{data['floor']}: {data['number']}")

    def test_instance_string_with_number_and_coords(self):
        data = {
            'number': 1,
            'coords': 4
        }

        slot = Slot.objects.create(**data)
        coords_dict = dict(Slot.coords_choices)

        self.assertEqual(str(slot), f"{coords_dict[data['coords']]}: {data['number']}")

    def test_instance_string_with_number_and_floor_and_coords(self):
        data = {
            'number': 1,
            'floor': 2,
            'coords': 4
        }

        slot = Slot.objects.create(**data)
        coords_dict = dict(Slot.coords_choices)

        self.assertEqual(str(slot), f"{coords_dict[data['coords']]}: {data['floor']}: {data['number']}")
