

from django.db import models
from api.models.propos.personnelles import Personnelles
from api.models.fonction.poste import Postes
from api.models.fonction.service import Services
from api.models.fonction.modefinancement import ModeFinancement


class Fonctions(models.Model):
    nom     = models.CharField()
    is_chef = models.BooleanField(default=False)
    service = models.ForeignKey(
        Services,
        on_delete=models.CASCADE,
        related_name="fonctions"
    )

    financement = models.ForeignKey(
        ModeFinancement,
        on_delete=models.CASCADE,null=True,
        related_name="financement"
    )

    chef_direct = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordonnes'
    )

    chef_direct = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subordonnes'
    )

    def __str__(self):
        return f"{self.nom}"
