from django.db import models
from api.models.propos.personnelles import Personnelles
from api.models.fonction.fonctions import Fonctions

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
    fonction = models.ForeignKey(
        Fonctions,
        on_delete=models.CASCADE,
        related_name="passations_services"
    )

    # Le Remplaçant : C'est aussi une clé vers Personnelles
    # On met null=True au cas où le remplaçant n'est pas encore désigné
    remplacant = models.ForeignKey(
        Personnelles,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passations_en_tant_que_remplacant'
    )

    # Champs de suivi automatiques
    created_at = models.DateTimeField(auto_now_add=True)

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