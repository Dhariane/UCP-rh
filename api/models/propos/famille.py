from api.models import  Personnelles
from django.db import models

class Famille(models.Model):
    nomPere= models.CharField(
        max_length=255,
        null= True,
        blank=True
    )
    nomMere= models.CharField(
        max_length=255,
        null= True,
        blank=True
    )
    nomConjoint= models.CharField(
        max_length=100,
        null= True,
        blank=True
    )
    prenomConjoint= models.CharField(
        max_length=100,
        null= True,
        blank=True
    )
    telConjoint= models.CharField(
        max_length=100,
        null= True,
        blank=True
    )
    adresseConjoint= models.CharField(
        max_length=100,
    )
    emailConjoint = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
    )
    nombreEnfant= models.CharField(
        max_length=100,
        null= True,
        blank=True
    )
    acteMariage=models.FileField(
        upload_to='acteMariage/'
    )
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.CASCADE, 
        related_name="Famille")