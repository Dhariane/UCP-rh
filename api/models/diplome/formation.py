from api.models import Personnelles
from django.db import models

class Formation(models.Model):

    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.PROTECT, 
        related_name="Formation")
    titre= models.TextField(

     )
    organisme= models.CharField(
        max_length=100
    )
    datedebut= models.DateField()
    datefin= models.DateField()
    attestation=models.ImageField(upload_to='attestation/')