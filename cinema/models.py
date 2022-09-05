from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from phonenumber_field.modelfields import PhoneNumberField
import re
from django.core.exceptions import ValidationError


class Movie(models.Model):
    name = models.CharField(max_length=50)
    poster = models.ImageField(upload_to='images', blank=True, null=True)
    description = models.CharField(max_length=1000)
    imdb_id = models.CharField(max_length=30)
    trailer_link = models.CharField(max_length=150)
    length = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    @cached_property
    def imdb_link(self):
        return 'https://www.imdb.com/title/' + str(self.imdb_id)

    @cached_property
    def embed_trailer(self):
        return str(self.trailer_link).replace('watch?v=', 'embed/')


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

    @cached_property
    def number(self):
        return int(self.code[1:])


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
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=None)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, default=None)
    hall = models.ForeignKey(CinemaHall, on_delete=models.CASCADE, default=None)
    playing_time = models.DateTimeField()

    def __str__(self):
        return f'{self.movie} playing in {self.cinema} on {self.playing_time}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['cinema', 'hall', 'playing_time'],
                name='unique_schedule'
            )
        ]

    @cached_property
    def end_time(self):

        end_time = self.playing_time
        parsed_time = re.findall(r'\d+[ ]?', self.movie.length)

        end_time += timezone.timedelta(
            hours=int(parsed_time[0]),
            minutes=int(parsed_time[1]),
        )

        return end_time

    def clean(self):

        if self.playing_time <= timezone.now():
            raise ValidationError('You can\'t schedule a movie in the past!')
            