from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from cinema.models import Movie, Schedule
from reservation.forms import ReservationForm


@login_required
def reservation_options(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    schedule_list = Schedule.objects.filter(
        movie=movie,
        playing_time__gt=timezone.now()
    ).order_by('playing_time')
    form = ReservationForm()
    if form.is_valid():
        form.save(commit=False)
        form.user_name = request.user
        form.save()

    context = {
        'movie': movie,
        'schedule': schedule_list,
        'form': form,
    }

    return render(request, 'reservation/reservation_options.html', context)
