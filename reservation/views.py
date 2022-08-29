from datetime import datetime
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from ratelimit.decorators import ratelimit
from cinema.models import Movie, Schedule, Seat
from reservation.forms import ReservationFilterForm
from django.contrib import messages
from reservation.models import Reservation


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def reservation_options(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = ReservationFilterForm(movie_id=movie)
    schedule_list = None

    if request.method == 'POST':
        cinema = request.POST.get('cinema')
        schedule_list = Schedule.objects.filter(
            movie=movie,
            cinema=cinema,
            playing_time__gte=datetime.now()).order_by('playing_time')
    context = {
        'movie': movie,
        'schedule': schedule_list,
        'form': form,
    }

    return render(request, 'reservation/reservation_options.html', context)


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def select_seats(request, movie, schedule):
    movie_object = get_object_or_404(Movie, pk=movie)
    schedule_object = get_object_or_404(Schedule, pk=schedule)

    hall = schedule_object.hall
    seat_list = hall.seats.all()

    # Get the already booked seats, so we can block them in the template
    occupied_seat_ids = Reservation.objects.filter(
        details=schedule_object,
        expired=False,
    ).values_list('seat', flat=True)

    context = {
        'movie': movie_object,
        'schedule': schedule_object,
        'seats': seat_list,
        'occupied_seats': occupied_seat_ids,
    }

    # Check if the user posts any data besides the CSRF token
    if len(request.POST) < 2:
        messages.error(request, 'Please select at least one seat!')

    elif request.POST:

        selected_seats = request.POST.getlist('checkboxes')
        reservations = []

        for seat in selected_seats:

            seat_obj = Seat.objects.get(id=seat)
            user_reservation = Reservation.objects.create_reservation(
                user=request.user,
                details=schedule_object,
                seat=seat_obj,
            )

            reservations.append(user_reservation)

        confirm_reservation(request, reservations, schedule)
        return render(request, 'reservation/reservation_email_sent.html')

    return render(request, 'reservation/select_seats.html', context)


def success(request, group):

    reservations = list(map(int, group.split('-')))

    for reservation in reservations:
        Reservation.objects.filter(
            id=reservation
        ).update(confirmed=True)

    send_tickets(request, reservations)

    return render(request, 'reservation/success.html')


def send_tickets(request, reservations):
    subject, from_email, to = 'Your tickets', 'office@silverscreen.com', (request.user.email,)
    email_text = get_template('reservation/reservation_successful.html')

    tickets = [Reservation.objects.get(id=reservation) for reservation in reservations]

    context = {
        'user': request.user,
        'tickets': tickets,
    }

    html_content = email_text.render(context)
    msg = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=from_email,
        to=to
    )
    msg.send()


def confirm_reservation(request, reservations, schedule):
    subject, from_email, to = 'Confirm your reservation', 'office@silverscreen.com', (request.user.email,)
    email_text = get_template('reservation/confirm_reservation.html')

    user_reservations = [str(reservation.id) for reservation in reservations]
    group = '-'.join(user_reservations)

    context = {
        'user': request.user,
        'tickets': reservations,
        'schedule': schedule,
        'schedule_group': group,
    }

    html_content = email_text.render(context)
    msg = EmailMessage(
        subject=subject,
        body=html_content,
        from_email=from_email,
        to=to
    )
    msg.send()

