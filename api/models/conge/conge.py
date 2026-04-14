from django.db import models
from api.models.propos.personnelles import Personnelles
from api.models.conge.statut import Statut
from api.models.conge.typeConges import TypeConge
from api.models.conge.soldeConge import SoldeConge
class Conge(models.Model):

    Personnel = models.ForeignKey(Personnelles, on_delete=models.CASCADE, related_name='conges')
    typeConge = models.ForeignKey(TypeConge, on_delete=models.CASCADE,related_name='type_conge')
    soldeConge = models.ForeignKey(SoldeConge, on_delete=models.CASCADE,related_name='solde_conge')
    dateDebut = models.DateField()
    dateFin = models.DateField()
    nombreJours = models.IntegerField(blank=True, null=True)
    description =models.TextField(blank=True,null=True)
    statut = models.ForeignKey(Statut,on_delete=models.CASCADE,related_name='statut_conge')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.dateDebut and self.dateFin:
            self.nombre_jours = (self.dateFin - self.dateDebut).days + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.Personnel} - {self.typeConge}"