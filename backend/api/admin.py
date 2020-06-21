from django.contrib import admin

from api.models import (
    Slot,
    Reservation
)


class SlotAdmin(admin.ModelAdmin):
    list_display = ('number', 'floor', 'coords')
    list_filter = ('coords', 'floor')


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'slot', 'plate_number', 'reserved_from', 'reserved_to', 'deleted_at')
    search_fields = ('user__email', 'plate_number')


admin.site.register(Slot, SlotAdmin)
admin.site.register(Reservation, ReservationAdmin)
