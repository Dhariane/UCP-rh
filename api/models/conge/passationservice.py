from django.db import models
from api.models.propos.personnelles import Personnelles
from api.models.fonction.fonctions import Fonctions
from api.models.conge.statut import Statut

class PassationService(models.Model):
    # Dates : Utilise DateField (ou DateTimeField) sans auto_now pour garder le contrôle
    date_absence = models.DateField()
    date_reprise = models.DateField()
    date = models.DateField()
    
    # Le Titulaire (lié à Personnelles)
    titulaire = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name='passations_en_tant_que_titulaire'
    )
    
    # La Fonction (liée à ton modèle Fonctions)
    fonction = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )  
    
    remplacant = models.ForeignKey(
        Personnelles,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passations_en_tant_que_remplacant'
    )

    # Champs de suivi automatiques
    created_at = models.DateTimeField(auto_now_add=True)

    statut = models.ForeignKey(
        Statut,
        on_delete=models.PROTECT,
        related_name='passations_services_statut',
        default=None,  # Ou mettre l'ID par défaut si connu
        null=True,
        blank=True
    )
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.statut_id:  # Nouvelle instance sans statut défini
            self.statut = Statut.objects.get(libelle="En attente")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    # Méthode pour calculer la durée dynamiquement
    @property
    def duree_absence(self):
        if self.date_absence and self.date_reprise:
            delta = self.date_reprise - self.date_absence
            return delta.days
        return 0

    def __str__(self):
        return f"Passation de {self.titulaire.nom} - {self.date_absence}"