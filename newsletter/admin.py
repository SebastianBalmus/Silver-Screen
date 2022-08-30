from django.contrib import admin
from django.contrib.admin import ModelAdmin

from newsletter.models import SubscribedUser
# Register your models here.


@admin.register(SubscribedUser)
class SubscribedUserAdmin(ModelAdmin):

    list_display = (
        'email',
    )

    search_fields = (
        'email',
    )
