from django.db import models
from api.models.propos.personnelles import Personnelles

class Experience(models.Model):
    
    entreprise= models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    poste=models.CharField(
        max_length=100,
        null=False,
        blank=False
    )

    datedebut=models.DateField()

    datefin=models.DateField(
        null=True,
        blank=True
    )

    description=models.TextField(
        null=True,
        blank=True
    )

    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.CASCADE, 
        related_name="Experience"
    )