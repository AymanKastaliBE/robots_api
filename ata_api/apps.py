from django.apps import AppConfig


class AtaApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ata_api'

    def ready(self):
        import ata_api.signals