from django.db import models
from api.models.propos.personnelles import Personnelles
class BaseCins(models.Model):
    numeroCin = models.CharField(unique=True,max_length=12)
    dateCin = models.DateField()
    lieuCin = models.CharField(max_length=100)
    numeroDuplicata = models.CharField(max_length=50, blank=True, null=True)
    dateDuplicata = models.DateField(blank=True, null=True)
    lieuDuplicata = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        abstract = True