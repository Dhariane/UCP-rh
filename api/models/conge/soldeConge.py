from django.db import models
from datetime import date
from api.models.propos.personnelles import Personnelles

class SoldeConge(models.Model):
    personnel = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name='soldes_conge'
    )
    annee = models.PositiveIntegerField()
    total = models.PositiveIntegerField(default=0)
    utilise = models.PositiveIntegerField(default=0)
    reste = models.PositiveIntegerField(default=0)
    is_manual = models.BooleanField(default=False)

    MAX_SOLDE = 72

    class Meta:
        unique_together = ('personnel', 'annee')

    def __str__(self):
        return f"{self.personnel} - {self.annee}"

    def calcul_total(self):
        today = date.today()

        if self.annee > today.year:
            return 0

        # Récupérer la date d'embauche depuis Fonctions
        from api.models.fonction.fonctions import Fonctions
        fonction = Fonctions.objects.filter(
            personnelle=self.personnel
        ).order_by('dateDebut').first()

        # Si pas de fonction → 0
        if not fonction or not fonction.dateDebut:
            return 0

        date_debut = fonction.dateDebut

        # Avant l'embauche → 0
        if self.annee < date_debut.year:
            return 0

        # Année courante
        if self.annee == today.year:
            if date_debut.year == today.year:
                # Embauché cette année → compter depuis le mois d'embauche
                mois_travailles = today.month - date_debut.month + 1
            else:
                # Embauché avant → tous les mois jusqu'à aujourd'hui
                mois_travailles = today.month

        # Année passée complète
        else:
            if self.annee == date_debut.year:
                # Année d'embauche → mois partiels
                mois_travailles = 12 - date_debut.month + 1
            else:
                mois_travailles = 12

        return min(max(mois_travailles, 0) * 2, self.MAX_SOLDE)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)

        if update_fields is None:
            # Recalcul automatique seulement si pas manuel
            if not self.is_manual:
                self.total = self.calcul_total()

            # Plafond 72j
            if self.total > self.MAX_SOLDE:
                self.total = self.MAX_SOLDE

            if self.utilise < 0:
                self.utilise = 0

            if self.utilise > self.total:
                self.utilise = self.total

            self.reste = self.total - self.utilise

        super().save(*args, **kwargs)