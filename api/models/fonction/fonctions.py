from django.db import models
from api.models.propos.personnelles import Personnelles
from api.models.fonction.poste import Postes
from api.models.fonction.service import Services


class Fonctions(models.Model):
    dateDebut = models.DateField()
    dateFin = models.DateField(null=True, blank=True)

    personnelle = models.ForeignKey(
        Personnelles,
        on_delete=models.PROTECT,
        related_name="fonctions"
    )

    poste = models.ForeignKey(
        Postes,
        on_delete=models.PROTECT,
        related_name="fonctions"
    )

    service = models.ForeignKey(
        Services,
        on_delete=models.PROTECT,
        related_name="fonctions"
    )

    def __str__(self):
        return f"{self.personnelle} | {self.poste} | {self.dateDebut}"
