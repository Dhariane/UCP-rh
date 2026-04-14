from django.db import models
from api.models.propos.personnelles import Personnelles  # Ajustez l'import selon votre structure

class Permissions(models.Model):
    # Relation avec votre table Personnelles
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.CASCADE, 
        related_name="permissions"
    )
    
    # Dates de l'absence
    date_debut = models.DateField()
    date_fin = models.DateField()
    
    # Détails de la demande
    motif = models.TextField()
    
    # Suivi de l'état (par défaut 'En attente')
    STATUT_CHOICES = [
        ('Approuvé', 'Approuvé'),
        ('Refusé', 'Refusé'),
    ]
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='Approuvé'
    )
    
    # Audit
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Permission: {self.personnelle.nom} {self.personnelle.prenom} ({self.date_debut})"

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"