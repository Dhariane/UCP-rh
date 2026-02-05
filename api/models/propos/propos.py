
from api.models.propos.etatCivils import EtatCivil
from django.db import models

class Propos(models.Model):

    nifStat = models.CharField(
        max_length=50,
    )

    numeroCnaps = models.CharField(
        max_length=50,
    )

    tel = models.CharField(
        max_length=50,
    )

    email = models.EmailField(
        max_length=100,
    )

    nombreEnfant = models.IntegerField(
    )


    etatCivil = models.ForeignKey(
        EtatCivil,
        on_delete=models.PROTECT,
        related_name="propos"
    )



    def __str__(self):
        return f"Propos #{self.id}"
