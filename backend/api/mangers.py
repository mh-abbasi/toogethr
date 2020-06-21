from django.db import models


class ReservationQuerySet(models.QuerySet):
    def filter_by_range(self, reserved_from, reserved_to):
        queryset = self

        if reserved_from:
            queryset = queryset.filter(
                models.Q(reserved_from__gte=reserved_from) |
                models.Q(reserved_to__gte=reserved_from)
            )

        if reserved_to:
            queryset = queryset.filter(
                models.Q(reserved_from__lte=reserved_to) |
                models.Q(reserved_to__lte=reserved_to)
            )

        return queryset
