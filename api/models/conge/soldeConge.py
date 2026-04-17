from django.db import models
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
        verbose_name = "Solde de congé"
        verbose_name_plural = "Soldes de congé"

    def __str__(self):
        return f"{self.personnel} - {self.annee}"

    def save(self, *args, **kwargs):
        self.reste = self.total - self.utilise
        super().save(*args, **kwargs)