from django.db.models.signals import post_save
from django.dispatch import receiver
from cinema.models import CinemaHall, Seat
from cinema.seatcodes import ALPHABET


@receiver(post_save, sender=CinemaHall)
def generate_seats(sender, instance, created, **kwargs):

    if created:

        seat_codes = [
            f'{ALPHABET.get(iterator//10+1)}{iterator%10+1}'
            for iterator in range(instance.number_of_seats)
        ]

        if not Seat.objects.filter(code='A1', hall=instance).exists():
            for code in seat_codes:

                seat = Seat(
                    hall=instance,
                    code=code,
                    occupied=False
                )
                seat.save()
