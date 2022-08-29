from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from cinema.models import Schedule, Seat


class ReservationManager(models.Manager):
    def create_reservation(self, user, details, seat):
        reservation = self.create(
            user=user,
            details=details,
            seat=seat,
            time_created=timezone.now()
        )
        return reservation


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)
    objects = ReservationManager()

    def __str__(self):
        return self.user.username + ' - ' + str(self.details)
