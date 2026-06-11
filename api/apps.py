from django.apps import AppConfig
import os


class ApiConfig(AppConfig):
    name = 'api'

    def ready(self):
        # Évite le double démarrage en développement
        if os.environ.get('RUN_MAIN') != 'true':
            try:
                from apscheduler.schedulers.background import BackgroundScheduler
                from apscheduler.triggers.cron import CronTrigger
                from api.tasks import rappel_solde_conge

                scheduler = BackgroundScheduler()
                scheduler.add_job(
                    rappel_solde_conge,
                    trigger=CronTrigger(day_of_week='mon', hour=8, minute=0),
                    id='rappel_solde_conge',
                    replace_existing=True,
                )
                scheduler.start()
                print("✅ Scheduler démarré — rappel congés tous les lundis 8h00")
            except Exception as e:
                print(f"⚠️ Erreur démarrage scheduler : {e}")