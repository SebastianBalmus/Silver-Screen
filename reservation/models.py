from django.contrib.auth.models import User
from django.db import models
from smart_selects.db_fields import ChainedForeignKey, ChainedManyToManyField

from cinema.models import Schedule, Seat


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    seat = ChainedForeignKey(
        Seat,
        chained_field='details',
        chained_model_field='hall',
        # show_all=False,
        # sort=True,
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'user__username'
