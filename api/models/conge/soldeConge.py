from django.db import models
from datetime import date, datetime
from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from api.models.propos.personnelles import Personnelles


class SoldeConge(models.Model):
    personnel = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name='soldes_conge'
    )
    annee          = models.PositiveIntegerField()
    total          = models.PositiveIntegerField(default=0)
    utilise        = models.PositiveIntegerField(default=0)
    reste          = models.PositiveIntegerField(default=0)
    is_manual      = models.BooleanField(default=False)

    MAX_SOLDE = 72

    class Meta:
        unique_together = ('personnel', 'annee')

    def __str__(self):
        return f"{self.personnel} - {self.annee}"

    # ──────────────────────────────────────────────────────────────────────────
    # Recalcule utilise via SUM dynamique, puis sauvegarde.
    # Appelé uniquement par les anciens chemins (hors signal congé planifié).
    # ──────────────────────────────────────────────────────────────────────────
    def mettre_a_jour_utilisation(self):
        from api.models.conge.congePlanifieModel import CongePlanifie

        total_recupere = CongePlanifie.objects.filter(
            personnel=self.personnel,
            date_debut__year=self.annee
        ).aggregate(total_jours=Sum('nombre_jours'))['total_jours'] or 0

        self.utilise = total_recupere
        self.save()

    # ──────────────────────────────────────────────────────────────────────────
    # Calcule le total théorique (mois_travailles × 2) à partir du 1er contrat.
    # Utilisé par save() quand is_manual=False.
    # ──────────────────────────────────────────────────────────────────────────
    def calcul_total(self):
        today = date.today()

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

        if self.annee < date_debut.year:
            return 0

        if self.annee == date_debut.year:
            mois_travailles = 12 - date_debut.month + 1
        else:
            mois_travailles = 12

        return min(max(mois_travailles, 0) * 2, self.MAX_SOLDE)

    # ──────────────────────────────────────────────────────────────────────────
    # save() standard — déclenché par mettre_a_jour_utilisation() et les
    # créations normales. NE PAS appeler depuis les signals congé planifié
    # (risque de boucle + écrasement du total bonifié).
    # ──────────────────────────────────────────────────────────────────────────
    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)

        if update_fields is None:
            if not self.is_manual:
                self.total = self.calcul_total()

            if self.total > self.MAX_SOLDE:
                self.total = self.MAX_SOLDE

            if self.utilise < 0:
                self.utilise = 0

            if self.utilise > self.total:
                self.utilise = self.total

            self.reste = self.total - self.utilise

        super().save(*args, **kwargs)


# ─────────────────────────────────────────────────────────────────────────────
# SIGNAL : nouveau Contrat → crée le SoldeConge de l'année de début
# ─────────────────────────────────────────────────────────────────────────────
from api.models.fonction.contrat import Contrat

@receiver(post_save, sender=Contrat)
def generer_solde_nouveau_contrat(sender, instance, created, **kwargs):
    """Crée un solde d'office dès qu'un nouveau contrat est enregistré."""
    if created and instance.personnelle and instance.dateDebut:
        if isinstance(instance.dateDebut, str):
            annee_contrat = int(instance.dateDebut.split('-')[0])
        else:
            annee_contrat = instance.dateDebut.year

        SoldeConge.objects.get_or_create(
            personnel=instance.personnelle,
            annee=annee_contrat
        )


# ─────────────────────────────────────────────────────────────────────────────
# SIGNAL : post_save CongePlanifie
#   - created=True  → recalcule utilise + crédite +2 jours (droit mensuel)
#   - created=False → recalcule uniquement utilise (modification sans bonus)
#
# On utilise QuerySet.update() pour éviter de re-déclencher SoldeConge.save()
# qui écraserait le total bonifié via calcul_total().
# ─────────────────────────────────────────────────────────────────────────────
def update_solde_on_save(sender, instance, created, **kwargs):
    from api.models.conge.congePlanifieModel import CongePlanifie

    annee_conge = instance.date_debut.year

    solde, _ = SoldeConge.objects.get_or_create(
        personnel=instance.personnel,
        annee=annee_conge
    )

    # ── 1. Recalcul de utilise via SUM dynamique ──────────────────────────
    total_utilise = CongePlanifie.objects.filter(
        personnel=instance.personnel,
        date_debut__year=annee_conge
    ).aggregate(total_jours=Sum('nombre_jours'))['total_jours'] or 0

    # ── 2. Bonus +2 jours mensuel uniquement à la création ───────────────
    DROIT_MENSUEL = 2

    if created:
        nouveau_total = min(solde.total + DROIT_MENSUEL, SoldeConge.MAX_SOLDE)
    else:
        nouveau_total = solde.total   # modification → pas de bonus supplémentaire

    nouveau_reste = max(0, nouveau_total - total_utilise)

    # ── 3. UPDATE direct — contourne SoldeConge.save() ───────────────────
    SoldeConge.objects.filter(pk=solde.pk).update(
        total=nouveau_total,
        utilise=total_utilise,
        reste=nouveau_reste,
    )


# ─────────────────────────────────────────────────────────────────────────────
# SIGNAL : post_delete CongePlanifie
#   - Restitue les jours du congé supprimé
#   - Annule le crédit +2 qui avait été accordé à la création
# ─────────────────────────────────────────────────────────────────────────────
def update_solde_on_delete(sender, instance, **kwargs):
    from api.models.conge.congePlanifieModel import CongePlanifie

    annee_conge = instance.date_debut.year

    try:
        solde = SoldeConge.objects.get(
            personnel=instance.personnel,
            annee=annee_conge
        )
    except SoldeConge.DoesNotExist:
        return

    # ── 1. Recalcul de utilise APRÈS suppression (l'instance est déjà retirée)
    total_utilise = CongePlanifie.objects.filter(
        personnel=instance.personnel,
        date_debut__year=annee_conge
    ).aggregate(total_jours=Sum('nombre_jours'))['total_jours'] or 0

    # ── 2. Annule le crédit +2 accordé lors de la création ───────────────
    DROIT_MENSUEL = 2
    nouveau_total = max(0, solde.total - DROIT_MENSUEL)
    nouveau_reste = max(0, nouveau_total - total_utilise)

    # ── 3. UPDATE direct — contourne SoldeConge.save() ───────────────────
    SoldeConge.objects.filter(pk=solde.pk).update(
        total=nouveau_total,
        utilise=total_utilise,
        reste=nouveau_reste,
    )