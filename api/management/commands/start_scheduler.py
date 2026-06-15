from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from api.tasks import rappel_solde_conge
import time


class Command(BaseCommand):
    help = 'Démarre le scheduler pour les tâches périodiques'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()

        # ✅ Tous les lundis à 8h00
        scheduler.add_job(
            rappel_solde_conge,
            trigger=CronTrigger(day_of_week='mon', hour=8, minute=0),
            id='rappel_solde_conge',
            replace_existing=True,
        )

        self.stdout.write('✅ Scheduler démarré — rappel tous les lundis à 8h00')
        scheduler.start()

        try:
            while True:
                time.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            self.stdout.write('Scheduler arrêté.')