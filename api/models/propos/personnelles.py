from django.db import models
from api.models.utils.baseNom import BaseNom
from api.models.propos.sexe import Sexes


class Personnelles(BaseNom):
    # Define fields for the Personnelles model here
    prenom = models.CharField(
        max_length=200
    )
    
    dateNaissance = models.DateField()

    lieuNaissance = models.CharField(
        max_length=200
    )
    sexe = models.ForeignKey(
        Sexes, 
        on_delete=models.PROTECT,
        related_name="personnelles"
    )
    adresse = models.CharField(
        max_length=255, 
        null=True, 
        blank=True
    )
    photoResidence = models.ImageField(
        upload_to='residences/',
        null=True,
        blank=True
    )
    telPerso = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    emailPerso = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        unique=True
    )
    cinphoto=models.FileField(
        upload_to='photocin/'
    )

    acteNaissance=models.FileField(
        upload_to='acteNaissance/'
    )

    casierjudiciaire=models.FileField(
        upload_to='Casierjudiciaire/'
    )
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    