from django.utils import timezone
from django.utils.translation import ugettext as _

from rest_framework import generics
from rest_framework.exceptions import ValidationError

from api.models import Slot, Reservation
from parking_lot.permissions import IsSuperUserOrReadOnly
from api.serializers import SlotSerializer


class SlotsAPIView(generics.ListCreateAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [IsSuperUserOrReadOnly]
    filterset_fields = ['number', 'floor', 'coords']

    @staticmethod
    def get_empty_slots(queryset, from_datetime, to_datetime):
        if not from_datetime and not to_datetime:
            raise ValidationError({
                'empty': [_('A date range must be set.')],
                'from_datetime': [_('A date range must be set.')],
                'to_datetime': [_('A date range must be set.')]
            })

        reservations_queryset = Reservation.objects.filter(deleted_at__isnull=True)
        reservations_queryset = reservations_queryset.filter_by_range(from_datetime, to_datetime)
        reserved_slots_id = reservations_queryset.values_list('slot_id', flat=True)

        queryset = queryset.exclude(id__in=reserved_slots_id)

        return queryset

    def get_queryset(self):
        empty = self.request.query_params.get('empty', 'false')
        from_datetime = self.request.query_params.get('from_datetime', None)
        to_datetime = self.request.query_params.get('to_datetime', None)

        if empty.lower() in ('1', 't', 'true', 'yes', 'y'):
            empty = True
        else:
            empty = False

        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(deleted_at__isnull=True)

        if empty:
            queryset = self.get_empty_slots(queryset, from_datetime, to_datetime)

        return queryset


class SlotItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slot.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [IsSuperUserOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(deleted_at__isnull=True)

        return queryset

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()

        Reservation.objects.filter(
            slot_id=instance.id
        ).update(
            deleted_at=timezone.now()
        )
