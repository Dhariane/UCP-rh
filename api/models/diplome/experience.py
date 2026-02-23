from django.db import models
from api.models.propos.personnelles import Personnelles

class Experience(models.Model):
    nombreExperience=models.IntegerField()
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
    datefin=models.DateField()
    description=models.TextField()
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.PROTECT, 
        related_name="Experience")