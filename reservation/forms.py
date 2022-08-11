from django import forms
from django.forms import ModelForm
from django.utils import timezone
from django.db.models import F, Func, CharField, Value
from reservation.models import Reservation
from cinema.models import Schedule, Seat, Cinema


class ReservationForm(ModelForm):

    class Meta:
        model = Reservation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['details'].queryset = Schedule.objects.filter(playing_time__gt=timezone.now())
        print(kwargs)

        self.fields['seat'].queryset = Seat.objects.filter(hall__name='details__hall')


class ReservationFilterForm(forms.Form):
    cinema = forms.ModelChoiceField(queryset=Cinema.objects.all())

    def __init__(self, movie_id):
        super().__init__()
        self.fields['cinema'].queryset = Cinema.objects.filter(
            schedule__movie=movie_id,
            schedule__playing_time__gte=timezone.now()
        ).distinct()
