from django.db import models
from api.models.utils.baseNom import BaseNom
from api.models.propos.sexe import Sexes

class Personnelles(BaseNom):
    # Define fields for the Personnelles model here
    prenom = models.CharField(max_length=200)
    dateNaissance = models.DateField()
    lieuNaissance = models.CharField(max_length=200)
    sexe = models.ForeignKey(Sexes, on_delete=models.PROTECT, related_name="personnelles")
    propos = models.ForeignKey("Propos", on_delete=models.SET_NULL, null=True, blank=True, related_name="personnelles")
    cin = models.ForeignKey("Cins", on_delete=models.SET_NULL, null=True, blank=True, related_name="personnelles")

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    