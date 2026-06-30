from django.apps import AppConfig
import os


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # ── C'EST ICI QU'ON FORCE DJANGO À CHARGER TES SIGNAUX ──
        import api.signal.conge_signal
