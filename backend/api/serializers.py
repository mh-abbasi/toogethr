from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import ugettext as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from user.serializers import UserProfileSerializer

from api.models import Slot, Reservation


class SlotSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField(
        required=True,
        allow_null=False,
        validators=[
            UniqueValidator(
                queryset=Slot.objects.filter(deleted_at__isnull=True)
            )
        ]
    )
    coords_title = serializers.CharField(
        read_only=True,
        source='get_coords_display'
    )

    class Meta:
        model = Slot
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        required=False,
        allow_null=True,
        write_only=True
    )
    user_data = UserProfileSerializer(
        source='user',
        read_only=True
    )
    slot = serializers.PrimaryKeyRelatedField(
        queryset=Slot.objects.filter(deleted_at__isnull=True),
        allow_null=False,
        required=True,
        write_only=True
    )
    slot_data = SlotSerializer(
        source='slot',
        read_only=True
    )
    
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate_user_change(self, data):
        request_user = self.context['request'].user

        if not request_user.is_superuser and 'user' in data and data['user'].id != request_user.id:
            raise ValidationError({
                'user': [_('You can\'t add reservations for another user.')],
            })

        if 'user' not in data:
            data['user'] = request_user

        return data

    def validate_date_range(self, data):
        reserved_from = data['reserved_from'] if 'reserved_from' in data else self.instance.reserved_from
        reserved_to = data['reserved_to'] if 'reserved_to' in data else self.instance.reserved_to

        if ('reserved_from' in data and reserved_from < timezone.now()) or \
                ('reserved_to' in data and reserved_to < timezone.now()):
            raise ValidationError({
                'reserved_from': [_('Reserved from value must be from now on.')],
                'reserved_to': [_('Reserved to value must be from now on.')]
            })

        if ('reserved_to' in data or 'reserved_from' in data) and reserved_from > reserved_to:
            raise ValidationError({
                'reserved_from': [_('The entered date range is invalid.')],
                'reserved_to': [_('The entered date range is invalid.')]
            })

    def validate_date_range_reserved(self, slot_id, reserved_from, reserved_to):
        queryset = Reservation.objects.filter(
            deleted_at__isnull=True,
            slot_id=slot_id
        ).filter_by_range(reserved_from, reserved_to)

        if self.instance:
            queryset = queryset.exclude(
                id=self.instance.id
            )

        return queryset.exists()

    def validate_date_range_and_slot(self, data):
        reserved_from = data['reserved_from'] if 'reserved_from' in data else self.instance.reserved_from
        reserved_to = data['reserved_to'] if 'reserved_to' in data else self.instance.reserved_to
        slot = data['slot'] if 'slot' in data else self.instance.slot_id

        if ('reserved_to' in data or 'reserved_from' in data or 'slot' in data) and \
                self.validate_date_range_reserved(slot, reserved_from, reserved_to):
            raise ValidationError({
                'slot': [_('This parking slot has been reserved for this time.')],
                'reserved_from': [_('This parking slot has been reserved for this time.')],
                'reserved_to': [_('This parking slot has been reserved for this time.')]
            })

    def validate(self, data):
        data = self.validate_user_change(data)
        self.validate_date_range(data)
        self.validate_date_range_and_slot(data)

        return data
