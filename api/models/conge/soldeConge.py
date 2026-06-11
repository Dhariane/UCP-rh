from django.db import models
<<<<<<< HEAD
from datetime import date, datetime
=======
from datetime import date
>>>>>>> 23088e43 (mon enregistrement local)
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

<<<<<<< HEAD
        # On ne calcule pas les soldes pour les années futures lointaines
        if self.annee > today.year:
            return 0

        from api.models.fonction.contrat import Contrat
        premier_contrat = Contrat.objects.filter(
            personnelle=self.personnel
        ).order_by('dateDebut').first()

        if not premier_contrat or not premier_contrat.dateDebut:
            return 0

        date_debut = premier_contrat.dateDebut

        if isinstance(date_debut, str):
            date_debut = datetime.strptime(date_debut, "%Y-%m-%d").date()

        # Si l'année demandée est avant son embauche → 0j
        if self.annee < date_debut.year:
            return 0

        # ── C'EST ICI QUE TOUT CHANGE POUR LE CUMUL DÈS LE DÉBUT DE L'ANNÉE ──
        
        # Cas 1 : C'est son année d'embauche
        if self.annee == date_debut.year:
            # On compte tous les mois restants du mois d'embauche jusqu'à décembre
            mois_travailles = 12 - date_debut.month + 1

        # Cas 2 : C'est une année après son embauche (ex: on calcule pour 2027 et il est venu en 2026)
        else:
            # Il est présent toute l'année, on lui donne ses 12 mois cumulés d'office !
            mois_travailles = 12

        # Calcul final (ex: 12 mois * 2j = 24j cumulés dès le 1er Janvier)
=======
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

>>>>>>> 23088e43 (mon enregistrement local)
        return min(max(mois_travailles, 0) * 2, self.MAX_SOLDE)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)

        if update_fields is None:
<<<<<<< HEAD
            if not self.is_manual:
                self.total = self.calcul_total()

=======
            # Recalcul automatique seulement si pas manuel
            if not self.is_manual:
                self.total = self.calcul_total()

            # Plafond 72j
>>>>>>> 23088e43 (mon enregistrement local)
            if self.total > self.MAX_SOLDE:
                self.total = self.MAX_SOLDE

            if self.utilise < 0:
                self.utilise = 0

            if self.utilise > self.total:
                self.utilise = self.total

            self.reste = self.total - self.utilise

<<<<<<< HEAD
        super().save(*args, **kwargs)


# ── SIGNALS DJANGO (Sortis de la classe et sécurisés) ──
from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models.fonction.contrat import Contrat

@receiver(post_save, sender=Contrat)
def generer_solde_nouveau_contrat(sender, instance, created, **kwargs):
    if created and instance.personnelle and instance.dateDebut:
        
        # 🛡️ SÉCURITÉ : On extrait l'année que la date soit un objet date ou une String
        if isinstance(instance.dateDebut, str):
            # Si c'est du texte '2026-06-08', on prend les 4 premiers caractères et on convertit en int
            annee_contrat = int(instance.dateDebut.split('-')[0])
        else:
            # Si c'est déjà un vrai objet date, on prend le .year directement
            annee_contrat = instance.dateDebut.year

        # On crée le solde l'esprit tranquille
        SoldeConge.objects.get_or_create(
            personnel=instance.personnelle,
            annee=annee_contrat
        )
=======
        super().save(*args, **kwargs)
>>>>>>> 23088e43 (mon enregistrement local)
