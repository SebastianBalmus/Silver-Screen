from django.contrib import admin
from reservation.models import Reservation


# Register your models here.
@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'details',
        'seat',
        'confirmed',
        'expired',
    )

    list_filter = (
        'confirmed',
        'details__playing_time'
    )
