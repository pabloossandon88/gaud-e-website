from django.apps import AppConfig


class GaudesiteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GaudeSite'


    def ready(self):
        import GaudeSite.signals

