from django.db import models
from api.models.propos.personnelles import Personnelles
from api.models.fonction.typeContrat import TypeContrats

class Contrat(models.Model):
    NumeroContrat = models.CharField(
        unique=True
    )
    periodeEssai = models.CharField(
        null=True
    )

    dateFinEssai = models.DateField(
        null=True,
        blank=True
    )

    photoContrat=models.FileField(
        upload_to='Contrats/'
    )
    salaire=models.CharField(
        null=True,
        blank=True
    )

    typeContrat = models.ForeignKey(
        TypeContrats,
        on_delete=models.CASCADE,
        related_name="typecontrats"
    )

    personnelle = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name="contrat"
    )