from django.apps import AppConfig
from django.db.models.signals import post_save


class CinemaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cinema'

    def ready(self):
        hall_model = self.get_model('CinemaHall')
        from . import signals
        post_save.connect(signals.generate_seats, sender=hall_model)
