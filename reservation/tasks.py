from django.db.models import F
from reservation.models import Reservation
from django.utils import timezone


def clear_unclaimed_reservations():
    reservations = Reservation.objects.annotate(
        time_until_playing=F('details__playing_time')-timezone.now()
    ).filter(
        time_until_playing__lte=timezone.timedelta(minutes=30),
        confirmed=False,
        expired=False
    )
    reservations.update(expired=True)
