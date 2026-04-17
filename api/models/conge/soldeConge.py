from django.db import models
from datetime import date
from api.models.propos.personnelles import Personnelles

class SoldeConge(models.Model):
    personnel = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name='soldes_conge'
    )
    annee = models.PositiveIntegerField()
    total = models.PositiveIntegerField(default=0)
    utilise = models.PositiveIntegerField(default=0)
    reste = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('personnel', 'annee')

    def __str__(self):
        return f"{self.personnel} - {self.annee}"

    # 🔥 +2 jours par mois
    def calcul_total(self):
        today = date.today()

        if self.annee < today.year:
            return 24
        elif self.annee == today.year:
            return today.month * 2
        else:
            return 0

    def save(self, *args, **kwargs):

        self.total = self.calcul_total()

        # 🔥 sécurité anti négatif
        if self.utilise < 0:
            self.utilise = 0

        if self.utilise > self.total:
            self.utilise = self.total

        self.reste = self.total - self.utilise

        super().save(*args, **kwargs)