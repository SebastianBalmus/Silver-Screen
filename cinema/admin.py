from cinema.forms import ScheduleForm
from django.contrib import admin
from .models import Cinema, CinemaHall, Contact, Movie, Schedule


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
