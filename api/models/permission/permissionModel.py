from django.db import models
from api.models.propos.personnelles import Personnelles

class Permissions(models.Model):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Approuvé', 'Approuvé'),
        ('Refusé', 'Refusé'),
    ]

    # Relation vers ton personnel (UCP-RH)
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.CASCADE, 
        related_name="permissions"
    )

    # Dates et heures de l'absence
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()

    # Justification
    motif = models.TextField()

    # --- CHAMPS DE CALCUL & TRAÇABILITÉ ---
    
    # Durée calculée de cette absence spécifique (ex: 1.5 jours)
    duree = models.FloatField(default=0)

    # Solde de l'employé AU MOMENT de la demande (ex: 40.0)
    solde_initial = models.FloatField(default=0)

    # Solde de l'employé APRÈS l'opération (ex: 38.5)
    solde_restant = models.FloatField(default=0)

    # État de la demande
    statut = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='En attente'
    )

    # Horodatage automatique
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Permission - {self.personnelle.nom} ({self.date_debut.strftime('%d/%m/%Y')})"