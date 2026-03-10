from api.models import Personnelles
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

class Formation(models.Model):

    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.PROTECT, 
        related_name="Formation"
    )

    titre= models.TextField()
    
    organisme= models.CharField(
        max_length=100
    )  
    lieu= models.CharField(
        max_length=100
    ) 

    annee = models.PositiveIntegerField(
    validators=[
        MinValueValidator(1900),
        MaxValueValidator(date.today().year)
    ]
)  

    attestation=models.FileField(
        upload_to='attestation/'
    )