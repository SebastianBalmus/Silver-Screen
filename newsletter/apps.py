from django.apps import AppConfig
from django.db.models.signals import post_save
from django.apps import apps


class NewsletterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsletter'

    def ready(self):
        movie_model = apps.get_model('cinema', 'Movie')
        from . import signals
        post_save.connect(signals.new_movie_added, sender=movie_model)
