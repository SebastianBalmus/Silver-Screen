from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import loader
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404
from ratelimit.decorators import ratelimit
from cinema.models import Movie, Schedule
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

        reservations = [
            Reservation(
                user=request.user,
                details=schedule_object,
                seat_id=seat_id
            ) for seat_id in selected_seats
        ]

        Reservation.objects.bulk_create(reservations)

        confirm_reservation(request, reservations, schedule)
        return render(request, 'reservation/reservation_email_sent.html')

    return render(request, 'reservation/select_seats.html', context)


def success(request, group):

    reservations = list(map(int, group.split('-')))

    Reservation.objects.filter(
        id__in=reservations
    ).update(confirmed=True)

    send_tickets(request, reservations)

    return render(request, 'reservation/success.html')


def send_tickets(request, reservations):
    subject, from_email, to = 'Your tickets', 'office@silverscreen.com', (request.user.email,)
    email_text = get_template('reservation/reservation_successful.html')

    tickets = Reservation.objects.filter(id__in=reservations)

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

    @login_required
    def my_reservations(request):
        reservations = Reservation.objects.filter(
            user=request.user
        ).order_by('-details__playing_time')

        paginator = Paginator(reservations, 10)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        context = {
            'reservations': page_object
        }

        return render(request, 'csv_management/my_reservations.html', context)

    @login_required
    def download_my_reservations(request):
        reservations = tuple(Reservation.objects.filter(
            user=request.user
        ).order_by('-details__playing_time'))

        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': f'attachment; filename="{request.user.username}_reservations.csv"'},
        )

        template = loader.get_template('csv_management/user_reservations.txt')

        context = {
            'data': reservations
        }

        response.write(template.render(context))
        return response


@login_required
def my_reservations(request):

    reservations = Reservation.objects.filter(
        user=request.user
    ).order_by('-details__playing_time')

    paginator = Paginator(reservations, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)

    context = {
        'reservations': page_object
    }

    return render(request, 'csv_management/my_reservations.html', context)


@login_required
def download_my_reservations(request):

    reservations = tuple(Reservation.objects.filter(
        user=request.user
    ).order_by('-details__playing_time'))

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{request.user.username}_reservations.csv"'},
    )

    template = loader.get_template('csv_management/user_reservations.txt')

    context = {
        'data': reservations
    }

    response.write(template.render(context))
    return response

