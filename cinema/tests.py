from django.test import TestCase
from cinema.models import Cinema, CinemaHall, Seat


class SeatGenerationTest(TestCase):

    def setUp(self) -> None:
        self.cinema = Cinema.objects.create(
            name='Test cinema',
            description='Used for testing',
            city='Test City',
            address='Test Street no. 5',
        )
        self.cinema.save()

    def test_hall_creation(self):
        self.hall = CinemaHall.objects.create(
            cinema=self.cinema,
            name='Test hall',
            number_of_seats=10,
        )
        self.hall.save()
        self.assertIsNotNone(self.hall)

    def test_seat_creation(self):
        self.hall = CinemaHall.objects.create(
            cinema=self.cinema,
            name='Test hall',
            number_of_seats=10,
        )
        self.hall.save()
        hall_seats = Seat.objects.filter(hall=self.hall)
        self.assertEqual(hall_seats[4].code, 'A5')

    def tearDown(self) -> None:
        self.cinema.delete()
