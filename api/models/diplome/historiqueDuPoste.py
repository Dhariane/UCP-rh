from api.models import Personnelles
from django.db import models

class HistoriqueDuPoste(models.Model):
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.PROTECT, 
        related_name="HistoriqueDuPoste")
    poste = models.CharField(
        max_length=100
    )
    société= models.CharField(
        max_length=100
    )
    datedebut=models.DateField()
    datefin=models.DateField()
    description=models.TextField()