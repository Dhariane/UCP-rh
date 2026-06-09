from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # ── C'EST ICI QU'ON FORCE DJANGO À CHARGER TES SIGNAUX ──
        import api.signal.conge_signal
