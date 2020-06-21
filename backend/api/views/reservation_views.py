from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.filtersets import ReservationFilter
from api.models import Reservation
from api.serializers import ReservationSerializer


class ReservationsAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ReservationFilter

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(user_id=self.request.user.id, deleted_at__isnull=True)

        return queryset


class ReservationItemAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            queryset = queryset.filter(user_id=self.request.user.id, deleted_at__isnull=True)

        return queryset

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
