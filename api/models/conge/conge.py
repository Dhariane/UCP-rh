from django.db import models
from django.core.exceptions import ValidationError
from api.models.propos.personnelles import Personnelles
from .typeConges import TypeConge
from .statut import Statut
from .soldeConge import SoldeConge

class Conge(models.Model):
    personnel = models.ForeignKey(
        Personnelles, 
        on_delete=models.CASCADE, 
        related_name='conges'
    )
    
    type_conge = models.ForeignKey(
        TypeConge, 
        on_delete=models.PROTECT,
        related_name='conges'
    )
    
    solde_conge = models.ForeignKey(
        SoldeConge, 
        on_delete=models.PROTECT,
        related_name='conges_utilises'
    )
    
    date_debut = models.DateField()
    date_fin = models.DateField()
    nombre_jours = models.PositiveIntegerField(editable=False)
    
    description = models.TextField(blank=True, null=True)
    statut = models.ForeignKey(
        Statut, 
        on_delete=models.PROTECT,
        related_name='conges'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    validated_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='conges_validated'
    )

    class Meta:
        verbose_name = "Congé"
        verbose_name_plural = "Congés"
        ordering = ['-created_at']

    def clean(self):
        if self.date_debut and self.date_fin:
            if self.date_fin < self.date_debut:
                raise ValidationError("La date de fin ne peut pas être avant la date de début")
            
            # Calcul du nombre de jours
            delta = (self.date_fin - self.date_debut).days + 1
            self.nombre_jours = delta

    def save(self, *args, **kwargs):
        self.clean()  # Validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.personnel} - {self.type_conge} ({self.date_debut} → {self.date_fin})"