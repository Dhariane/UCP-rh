from django.db import models
from api.models.propos.personnelles import Personnelles
from api.models.fonction.fonctions import Fonctions
from api.models.conge.statut import Statut
<<<<<<< HEAD
from api.models.fonction.contrat import Contrat
=======
>>>>>>> 23088e43 (mon enregistrement local)

class PassationService(models.Model):
    
    date_absence = models.DateField()
    date_reprise = models.DateField()
    date = models.DateField()
    
<<<<<<< HEAD
=======
    
>>>>>>> 23088e43 (mon enregistrement local)
    titulaire = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name='passations_en_tant_que_titulaire'
    )  
    
    remplacant = models.ForeignKey(
        Personnelles,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passations_en_tant_que_remplacant'
    )

<<<<<<< HEAD
=======
    
>>>>>>> 23088e43 (mon enregistrement local)
    created_at = models.DateTimeField(auto_now_add=True)

    statut = models.ForeignKey(
        Statut,
        on_delete=models.PROTECT,
        related_name='passations_services_statut',
        default=None,  
        null=True,
        blank=True
    )
    
<<<<<<< HEAD
=======
    
>>>>>>> 23088e43 (mon enregistrement local)
    fonction = models.ForeignKey(
        Fonctions,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='passations_services'
    )

    def save(self, *args, **kwargs):
        if not self.pk:  # Seulement à la création
            
<<<<<<< HEAD
            # ✅ CORRECTION — Passer par le Contrat actif pour avoir la fonction
            if self.titulaire:
                contrat_actif = Contrat.objects.filter(
                    personnelle=self.titulaire, 
                    is_actif=True
                ).first()
                
                if contrat_actif and contrat_actif.fonction:
                    self.fonction = contrat_actif.fonction
=======
            # ✅ CORRECTION — récupérer la fonction depuis le modèle Fonctions
            if self.titulaire:
                f = Fonctions.objects.filter(personnelle=self.titulaire).last()
                if f:
                    self.fonction = f  # ForeignKey vers Fonctions, pas .nom
>>>>>>> 23088e43 (mon enregistrement local)

            # Statut par défaut
            if not self.statut_id:
                try:
                    self.statut = Statut.objects.get(statut="En attente")
                except Statut.DoesNotExist:
                    raise ValueError("Le statut 'En attente' n'existe pas en base de données.")

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