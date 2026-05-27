
from django.db import models
from .typeDiplome import DiplomeType
from api.models import Personnelles


class Diplome(models.Model):
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.CASCADE, 
        related_name="diplomes"
    )
    
    type_diplome = models.ForeignKey(
        DiplomeType, 
        on_delete=models.PROTECT,
        related_name="diplomes",
        verbose_name="Type de diplôme"
    )
    
    filiere = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Filière"
    )
    lieu = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Lieu"
    )
    
    etablissement = models.CharField(max_length=100)
    anneeObtention = models.PositiveIntegerField(
        verbose_name="Année d'obtention",
        null=True, 
        blank=True
    )
    photo = models.FileField(
        upload_to='photos/', 
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = "Diplôme"
        verbose_name_plural = "Diplômes"
        ordering = ['-anneeObtention']

    def __str__(self):
        return f"{self.type_diplome} - {self.personnelle}"
