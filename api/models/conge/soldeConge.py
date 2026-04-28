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
    is_manual = models.BooleanField(default=False)  # ← nouveau champ

    MAX_SOLDE = 72  # ← plafond global

    class Meta:
        unique_together = ('personnel', 'annee')

    def __str__(self):
        return f"{self.personnel} - {self.annee}"

    def calcul_total(self):
        today = date.today()

        if self.annee < today.year:
            total_calcule = 24
        elif self.annee == today.year:
            total_calcule = today.month * 2
        else:
            return 0

        return min(total_calcule, self.MAX_SOLDE)  # ← plafond appliqué

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)

        if update_fields is None:
            # ✅ Recalcul automatique SEULEMENT si pas de saisie manuelle
            if not self.is_manual:
                self.total = self.calcul_total()

            # Plafond sur le total dans tous les cas
            if self.total > self.MAX_SOLDE:
                self.total = self.MAX_SOLDE

            if self.utilise < 0:
                self.utilise = 0

            if self.utilise > self.total:
                self.utilise = self.total

            self.reste = self.total - self.utilise

        super().save(*args, **kwargs)