from django.db import models
from api.models.fonction.service import Services
from api.models.propos.personnelles import Personnelles
from api.models.fonction.typeContrat import TypeContrats
from api.models.fonction.modefinancement import ModeFinancement
from api.models.fonction.fonctions import Fonctions 

class Contrat(models.Model):
    NumeroContrat = models.CharField(
        max_length=100, 
        unique=True
    )

    dateDebut = models.DateField()
    
    dateFin = models.DateField(
        null=True,
        blank=True
    )

    # Lien vers le rôle/fonction
    fonction = models.ForeignKey(
        Fonctions,
        on_delete=models.CASCADE,
        related_name="contrats"
    )

    service = models.ForeignKey(Services, on_delete=models.PROTECT)

    financement = models.ForeignKey(
        ModeFinancement,
        on_delete=models.PROTECT,  # Empêche la suppression du financement s'il est utilisé
        null=True,
        blank=True,
        related_name="contrats"
    )
    
    periodeEssai = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    dateFinEssai = models.DateField(
        null=True,
        blank=True
    )

    photoContrat = models.FileField(
        upload_to='Contrats/',
        null=True,
        blank=True
    )

    salaire = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        null=True, 
        blank=True
    )

    typeContrat = models.ForeignKey(
        TypeContrats,
        on_delete=models.PROTECT,
        related_name="contrats"
    )

    personnelle = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name="contrats"
    )

    class Meta:
        verbose_name = "Contrat"
        verbose_name_plural = "Contrats"
        ordering = ['-dateDebut']

    def __str__(self):
        return f"Contrat {self.NumeroContrat} - {self.personnelle}"
