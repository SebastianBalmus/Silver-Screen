from django.db import models
from datetime import timedelta

from django.utils import timezone
from django.utils.functional import cached_property
from phonenumber_field.modelfields import PhoneNumberField
from smart_selects.db_fields import ChainedForeignKey
import re
from django.core.exceptions import ValidationError


class Movie(models.Model):
    name = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='images')
    description = models.CharField(max_length=1000)
    imdb_id = models.CharField(max_length=30)
    trailer_link = models.CharField(max_length=150)
    length = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    @cached_property
    def imdb_link(self):
        return 'https://www.imdb.com/title/' + self.imdb_id.__str__()

    @cached_property
    def embed_trailer(self):
        return self.trailer_link.__str__().replace('watch?v=', 'embed/')


class Cinema(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=70)

    def __str__(self):
        return self.name


class CinemaHall(models.Model):
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='halls')
    name = models.CharField(max_length=30)
    number_of_seats = models.IntegerField()
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, related_name='seats')
    code = models.CharField(max_length=4, default='1A')
    occupied = models.BooleanField(default=False)

    def __str__(self):
        return f'Seat {self.code} in hall {str(self.hall)}'


class Contact(models.Model):
    name = models.CharField(max_length=40)
    email = models.EmailField()
    phone = PhoneNumberField()
    city = models.CharField(max_length=20, blank=True, null=True)
    cinema = models.CharField(max_length=30, blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1500)

    def __str__(self):
        return self.email


class Schedule(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    hall = ChainedForeignKey(
        CinemaHall,
        chained_field='cinema',
        chained_model_field='cinema',
        show_all=False,
        auto_choose=True,
        sort=True,
    )
    playing_time = models.DateTimeField()

    @cached_property
    def end_time(self):
        end_time = self.playing_time
        parsed_time = re.findall(r'\d+[ ]?', self.movie.length)

        end_hour = end_time.hour + int(parsed_time[0])
        end_minute = end_time.minute + int(parsed_time[1])

        if end_minute > 59:
            end_hour += 1
            end_minute -= 60

        if end_hour > 23:
            end_time = self.playing_time + timedelta(days=1)
            end_hour -= 24

        end_time = end_time.replace(
            hour=end_hour,
            minute=end_minute,
        )

        return end_time

    def clean(self):

        for obj in Schedule.objects.all():
            if (
                    self.cinema.name == obj.cinema.name
                    and self.hall.name == obj.hall.name
                    and self.playing_time <= obj.end_time
                    and self.end_time >= obj.playing_time
            ):
                raise ValidationError('There is a movie playing in that interval')

        if self.playing_time <= timezone.now():
            raise ValidationError('You can\'t schedule a movie in the past!')
