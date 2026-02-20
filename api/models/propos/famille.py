from api.models import  Personnelles
from django.db import models

class Famille(models.Model):
    nomPere= models.CharField(
        max_length=100,
        null= True,
        blank=True
    )
    prenomPere= models.CharField(
        max_length=100,
        null= True,
        blank=True
    )
    nomMere= models.CharField(
        max_length=100,
        null= True,
        blank=True
    )
    prenomMere= models.CharField(
        max_length=100,
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
    nombreEnfant= models.CharField(
        max_length=100,
        null= True,
        blank=True
    )
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.PROTECT, 
        related_name="Famille")