from django.urls import path

from api.views import (
    SlotsAPIView,
    SlotItemAPIView,
    ReservationsAPIView,
    ReservationItemAPIView
)

app_name = 'api'

urlpatterns = [
    path('slots', SlotsAPIView.as_view(), name='slots'),
    path('slots/<int:pk>', SlotItemAPIView.as_view(), name='slots_item'),

    path('reservations', ReservationsAPIView.as_view(), name='reservations'),
    path('reservations/<int:pk>', ReservationItemAPIView.as_view(), name='reservations_item'),
]
