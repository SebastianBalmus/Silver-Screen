from django.db import models
from django.utils.functional import cached_property

# Create your models here.


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


class Cinema(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    city = models.CharField(max_length=30)
    address = models.CharField(max_length=70)
    hall = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class CinemaHall(models.Model):
    name = models.CharField(max_length=30)
    seats = models.IntegerField()
    description = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Seat(models.Model):

    OCCUPIED = 'O'
    EMPTY = 'E'
    STATUS_CHOICES = [
        (OCCUPIED, 'Occupied'),
        (EMPTY, 'Empty')
    ]

    reservation = models.CharField(max_length=10, choices=STATUS_CHOICES, default=EMPTY)

