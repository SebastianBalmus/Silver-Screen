from django.http import HttpResponseRedirect
from django.shortcuts import render
from cinema.forms import ScheduleForm, CSVImportForm
from django.contrib import admin, messages
from .models import Cinema, CinemaHall, Contact, Movie, Schedule, Seat
from django.urls import path, reverse


class CinemaHallInline(admin.TabularInline):
    model = CinemaHall


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'subject',
    )

    list_filter = (
        'cinema',
        'city',
    )

    search_fields = [
        'message',
        'name',
        'subject',
    ]


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'city',
    )
    inlines = (CinemaHallInline,)


@admin.register(CinemaHall)
class CinemaHallAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cinema',
    )
    list_filter = (
        'seats',
    )
    search_fields = [
        'name',
        'cinema',
    ]


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'length',
    )

    search_fields = [
        'name',
        'description',
    ]

    change_list_template = 'cinema/admin/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload_movies/', self.upload_movies, name='upload_movies')
        ]

        return custom_urls + urls

    def upload_movies(self, request):

        if request.method == 'POST':
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                messages.warning(request, 'The wrong file type was uploaded')
                return HttpResponseRedirect(request.path_info)

            file_data = csv_file.read().decode('utf-8')
            csv_data = file_data.split('\n')

            for row in csv_data:
                fields = row.split(',')
                movie = Movie.objects.update_or_create(
                    name=fields[0],
                    description=fields[1],
                    imdb_id=fields[2],
                    trailer_link=fields[3],
                    length=fields[4],
                )

            url = reverse('admin:index')
            return HttpResponseRedirect(url)

        form = CSVImportForm()
        context = {'form': form}

        return render(request, 'cinema/admin/upload_movies.html', context)


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleForm
    list_display = (
        'movie',
        'cinema',
        'hall',
        'playing_time',
        'end_time',
    )

    class Media:
        js = (
            'js/admin_schedule.js',
        )


admin.site.register(Seat)