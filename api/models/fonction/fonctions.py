from django.db import models
from api.models.propos.personnelles import Personnelles
from api.models.fonction.poste import Postes
from api.models.fonction.service import Services
from api.models.fonction.superieurs import Superieur


class Fonctions(models.Model):
    nom = models.CharField()
    dateDebut = models.DateField()
    dateFin = models.DateField(
        null=True,
        blank=True
    )
    financement = models.CharField()

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
    superieur = models.ForeignKey(
        Superieur,
        on_delete=models.PROTECT,null=True,
        related_name="superieur"
    )

    def __str__(self):
        return f"{self.personnelle} | {self.poste} | {self.dateDebut}"
