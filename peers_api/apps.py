from django.apps import AppConfig


class PeersApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'peers_api'

    def ready(self) -> None:
        import peers_api.signals.handlers
