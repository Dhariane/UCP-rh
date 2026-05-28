from django.db import models
from django.core.exceptions import ValidationError
from api.models.propos.personnelles import Personnelles
from api.models.conge.typeConges import TypeConge 

class CongePlanifie(models.Model):
    personnel = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name='conges_planifies'
    )
    type_conge = models.ForeignKey(
        TypeConge,
        on_delete=models.PROTECT,
        related_name='conges_planifies'
    )
    date_debut = models.DateField()
    date_fin = models.DateField()
    
    # Ajout de null=True pour éviter les blocages de la base de données avant calcul
    nombre_jours = models.PositiveIntegerField(editable=False, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_conges_planifies'  # Parfaitement aligné avec tes tables Postgres
        ordering = ['date_debut']

    def clean(self):
        super().clean()
        if self.date_debut and self.date_fin:
            if self.date_fin < self.date_debut:
                raise ValidationError("La date de fin ne peut pas être antérieure à la date de début.")
            # Calcul automatique inclusif (ex: du 10 au 12 = 3 jours)
            self.nombre_jours = (self.date_fin - self.date_debut).days + 1

    def save(self, *args, **kwargs):
        # Force l'exécution de clean() pour valider les dates et calculer nombre_jours via l'API
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[Planifié] {self.personnel} ({self.date_debut} au {self.date_fin})"