from django_filters import rest_framework as filters

from api.models import Reservation


class ReservationFilter(filters.FilterSet):
    from_date = filters.DateTimeFilter(field_name="reserved_from", lookup_expr='gte')
    to_date = filters.DateTimeFilter(field_name="reserved_to", lookup_expr='lte')

    class Meta:
        model = Reservation
        fields = ['slot_id', 'user_id', 'from_date', 'to_date']

