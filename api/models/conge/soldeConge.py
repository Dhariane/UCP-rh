from django.db import models
from api.models.propos.personnelles import Personnelles

class SoldeConge(models.Model):
    Personnelles = models.ForeignKey(Personnelles, on_delete=models.CASCADE, related_name='soldes')
    annee = models.IntegerField()
    total = models.IntegerField()
    reste = models.IntegerField()

    def __str__(self):
        return f"{self.Personnelles} - {self.annee}"