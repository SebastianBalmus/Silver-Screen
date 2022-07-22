from django.contrib import admin
from .models import Contact, Movie


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'email',
                    'subject')

    list_filter = ('cinema', 'city')
    search_fields = [
        'message',
        'name',
        'subject',
    ]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Movie)
