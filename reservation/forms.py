from django import forms
from django.forms import ModelForm
from django.utils import timezone

from reservation.models import Reservation
from cinema.models import Schedule, Seat


class ReservationForm(ModelForm):

    class Meta:
        model = Reservation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['details'].queryset = Schedule.objects.filter(playing_time__gt=timezone.now())
        self.fields['seat'].queryset = Seat.objects.filter(hall__name='details__hall')
