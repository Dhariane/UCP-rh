
from api.models.propos.etatCivils import EtatCivil
from django.db import models

class Propos(models.Model):

    nifStat = models.CharField(
        max_length=50,
        db_column="nifStat",
        null=True,
        blank=True
    )

    numeroCnaps = models.CharField(
        max_length=50,
        db_column="numeroCnaps",
        null=True,
        blank=True
    )

    tel = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    email = models.EmailField(
        max_length=50,
        null=True,
        blank=True
    )

    nombreEnfant = models.IntegerField(
        db_column="nombreEnfant",
        null=True,
        blank=True
    )

    # 🔑 Clé étrangère
    etatCivile = models.ForeignKey(
        EtatCivile,
        on_delete=models.PROTECT,
        db_column="id_1",
        related_name="propos"
    )



    def __str__(self):
        return f"Propos #{self.id}"
