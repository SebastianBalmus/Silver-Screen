from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from .forms import ContactForm
from ratelimit.decorators import ratelimit
from cinema.models import Movie, Cinema
from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


# Homepage view
def home(request):
    return render(request, 'cinema/home.html')


# Contact view
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return render(request, 'cinema/home.html')
    else:
        contact_form = ContactForm()

    context = {'form': contact_form}
    return render(request, 'cinema/contact.html', context)


# Currently playing movies
def currently_playing(request):
    movie_list = Movie.objects.filter(
        schedule__isnull=False,
        schedule__playing_time__lte=timezone.now()+timezone.timedelta(days=6),
        schedule__playing_time__gt=timezone.now()
    ).distinct()
    paginator = Paginator(movie_list, 5)

    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'cinema/currently_playing.html', {'page_obj': page_object})


class HallList(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request, format=None):
        cinema = request.POST.get('cinema')
        hall = {}
        if cinema:
            halls = Cinema.objects.get(id=cinema).halls.all()
            hall = {item.name: item.id for item in halls}
        return JsonResponse(data=hall, safe=False)
