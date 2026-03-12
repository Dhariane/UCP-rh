from django.db import models
from api.models.utils.baseNom import BaseNom
from api.models.propos.personnelles import Personnelles

class Enfant(BaseNom):
    # Define fields for the Personnelles model here
    prenom = models.CharField(
        max_length=200
    )
    dateNaissance = models.DateField()

    lieuNaissance = models.CharField(
        max_length=200
    )
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.CASCADE, 
        related_name="Enfant"
    )
    
    certificatVie=models.FileField(
        upload_to='certificatVie/'
    )

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    