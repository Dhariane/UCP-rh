from django.db import models
from api.models.propos.personnelles import Personnelles
from api.models.fonction.typeContrat import TypeContrats

class Contrat(models.Model):
    NumeroContrat = models.CharField()

    photoContrat=models.FileField(
        upload_to='Contrats/'
    )

    typeContrat = models.ForeignKey(
        TypeContrats,
        on_delete=models.PROTECT,
        related_name="typecontrats"
    )

    personnelle = models.ForeignKey(
        Personnelles,
        on_delete=models.PROTECT,
        related_name="contrat"
    )