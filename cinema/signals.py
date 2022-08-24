from django.db.models.signals import post_save
from django.dispatch import receiver
from cinema.models import CinemaHall, Seat
from cinema.seatcodes import seat_codes


@receiver(post_save, sender=CinemaHall)
def generate_seats(sender, instance, created, **kwargs):

    if created:
        seats_per_row = 10
        number_of_rows = int(str(instance.number_of_seats)) // seats_per_row

        if not Seat.objects.filter(code='A1', hall=instance).exists():
            for row in range(number_of_rows):
                for column in range(seats_per_row):
                    code = f'{seat_codes.get(row+1)}{column+1}'
                    seat = Seat(
                        hall=instance,
                        code=code,
                        occupied=False,
                    )
                    seat.save()
