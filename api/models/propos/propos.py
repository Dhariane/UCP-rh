from api.models.propos.etatCivils import EtatCivil
from django.db import models

class Propos(models.Model):

    nif = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    stat = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    numeroCnaps = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    tel = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        unique=True
    )

    nombreEnfant = models.IntegerField(
        null=True,
        blank=True
    )

    etatCivil = models.ForeignKey(
        EtatCivil,
        on_delete=models.CASCADE,
        related_name="propos"
    )
    personnelle = models.ForeignKey(
        'Personnelles', 
        on_delete=models.CASCADE,
        related_name='propos_list'
    )

    def __str__(self):
        return f"Propos #{self.id}"
