from api.models import Personnelles
from django.db import models

class Diplome(models.Model):
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.CASCADE, 
        related_name="Diplome"
    )
    
    nom = models.CharField(
        max_length=100
    )

    etablissement= models.CharField(
        max_length=100
    )

    dateObtention=models.DateField()

    photo=models.FileField(
        upload_to='photos/'
    )