from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from reservation.models import Reservation
from django.core.paginator import Paginator


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
