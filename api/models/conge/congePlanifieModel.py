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
    date_debut   = models.DateField()
    date_fin     = models.DateField()
    nombre_jours = models.PositiveIntegerField(editable=False, blank=True, null=True)
    description  = models.TextField(blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_conges_planifies'
        ordering = ['date_debut']

    # ──────────────────────────────────────────────────────────────────────────
    # Validation + calcul nombre_jours
    # Appelé automatiquement par save() via full_clean()
    # ──────────────────────────────────────────────────────────────────────────
    def clean(self):
        super().clean()

        if self.date_debut and self.date_fin:

            # ── Cohérence des dates ───────────────────────────────────────────
            if self.date_fin < self.date_debut:
                raise ValidationError(
                    "La date de fin ne peut pas être antérieure à la date de début."
                )

            # ── Calcul inclusif (du 10 au 12 = 3 jours) ─────────────────────
            self.nombre_jours = (self.date_fin - self.date_debut).days + 1

            # ── Vérification du solde restant ─────────────────────────────────
            from api.models.conge.soldeConge import SoldeConge

            try:
                solde_actuel = SoldeConge.objects.get(
                    personnel=self.personnel,
                    annee=self.date_debut.year
                )
            except SoldeConge.DoesNotExist:
                raise ValidationError(
                    f"Aucun solde de congé n'a été initialisé "
                    f"pour l'année {self.date_debut.year}."
                )

            # Somme des jours déjà planifiés (on exclut cet enregistrement
            # en cas de modification pour éviter de se compter soi-même)
            jours_deja_pris = (
                CongePlanifie.objects.filter(
                    personnel=self.personnel,
                    date_debut__year=self.date_debut.year
                )
                .exclude(pk=self.pk)
                .aggregate(total=models.Sum('nombre_jours'))['total'] or 0
            )

            reste_disponible = solde_actuel.total - jours_deja_pris

            if self.nombre_jours > reste_disponible:
                raise ValidationError(
                    f"Solde insuffisant ! Vous demandez {self.nombre_jours} jour(s), "
                    f"mais il ne reste que {reste_disponible} jour(s) disponible(s) "
                    f"pour l'année {self.date_debut.year}."
                )

    # ──────────────────────────────────────────────────────────────────────────
    # save() — déclenche la validation puis persiste.
    # Les signals post_save / post_delete se chargent de mettre à jour
    # SoldeConge (utilise, total +2, reste) via UPDATE direct.
    # ──────────────────────────────────────────────────────────────────────────
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"[Planifié] {self.personnel} "
            f"({self.date_debut} au {self.date_fin})"
        )


# ─────────────────────────────────────────────────────────────────────────────
# CONNEXION EXPLICITE DES SIGNALS
# Importés depuis soldeConge.py pour éviter les imports circulaires au démarrage
# ─────────────────────────────────────────────────────────────────────────────
from django.db.models.signals import post_save, post_delete
from api.models.conge.soldeConge import update_solde_on_save, update_solde_on_delete

post_save.connect(update_solde_on_save,   sender=CongePlanifie)
post_delete.connect(update_solde_on_delete, sender=CongePlanifie)