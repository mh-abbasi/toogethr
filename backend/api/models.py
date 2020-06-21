from django.db import models
from django.utils.translation import ugettext as _

from api.mangers import ReservationQuerySet


class TimeAbstract(models.Model):
    """Extending the base model to have soft deletion feature"""
    created_at = models.DateTimeField(
        verbose_name=_('Created At'),
        auto_now_add=True,
        editable=False
    )
    modified_at = models.DateTimeField(
        verbose_name=_('Modified At'),
        auto_now=True,
        editable=False
    )

    deleted_at = models.DateTimeField(
        verbose_name=_('Deleted At'),
        null=True,
        blank=True,
        default=None,
        editable=False
    )

    class Meta:
        abstract = True


class Slot(TimeAbstract):
    """Slot model for parking lot"""

    # Coords choice for guiding drivers throught the lot
    coords_choices = (
        (1, _('North')),
        (2, _('North East')),
        (3, _('East')),
        (4, _('South East')),
        (5, _('South')),
        (6, _('South West')),
        (7, _('West')),
        (8, _('North West')),
    )

    number = models.PositiveSmallIntegerField(
        verbose_name=_('Number'),
        null=False,
        blank=False
    )
    floor = models.SmallIntegerField(
        verbose_name=_('Floor'),
        null=True,
        blank=True,
        default=0
    )
    coords = models.PositiveSmallIntegerField(
        verbose_name=_('Coords'),
        null=True,
        blank=True,
        choices=coords_choices
    )

    class Meta:
        verbose_name = _('Slot')
        verbose_name_plural = _('Slots')

    def __str__(self):
        slot_title_array = list()
        if self.coords:
            slot_title_array.append(self.get_coords_display())

        if self.floor:
            slot_title_array.append(str(self.floor))

        slot_title_array.append(str(self.number))

        return ': '.join(slot_title_array)


class Reservation(TimeAbstract):
    """Reservation model that contains slot bookings"""
    user = models.ForeignKey(
        verbose_name=_('User'),
        null=False,
        blank=False,
        to='user.User',
        on_delete=models.DO_NOTHING
    )
    slot = models.ForeignKey(
        verbose_name=_('Slot'),
        null=False,
        blank=False,
        to='api.Slot',
        on_delete=models.DO_NOTHING,
        related_name='reservations'
    )
    plate_number = models.CharField(
        verbose_name=_('Plate Number'),
        max_length=10,
        null=True,
        blank=True
    )
    reserved_from = models.DateTimeField(
        verbose_name=_('Reserved From'),
        null=False,
        blank=False
    )
    reserved_to = models.DateTimeField(
        verbose_name=_('Reserved To'),
        null=False,
        blank=False
    )

    objects = ReservationQuerySet.as_manager()

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')
        ordering = ['reserved_from']

    def __str__(self):
        return f"{self.slot} reserved by {self.user}"
