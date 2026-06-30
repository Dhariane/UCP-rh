from django.db import models
from api.models.propos.personnelles import Personnelles


class EvenementPermission(models.Model):
    """
    Référentiel des 7 événements. Alimenté via SQL.
    duree_defaut=None pour événements 6 & 7 (discrétion RH).
    """
    code = models.PositiveSmallIntegerField(unique=True)
    libelle = models.CharField(max_length=255)
    duree_defaut = models.FloatField(
        null=True, blank=True,
        help_text="Null = durée à discrétion RH"
    )
    est_fractionnable = models.BooleanField(default=False)
    delai_prise = models.PositiveSmallIntegerField(
        null=True, blank=True,
        help_text="Délai max en jours (ex: 15 pour naissance)"
    )

    class Meta:
        verbose_name = "Événement de permission"
        verbose_name_plural = "Événements de permission"
        ordering = ['code']

    def __str__(self):
        duree = f"{self.duree_defaut}j" if self.duree_defaut is not None else "Discrétion RH"
        return f"({self.code}) {self.libelle} — {duree}"


class SoldePermission(models.Model):
    """Solde annuel de 10j par employé. Réinitialisable par le RH."""
    SOLDE_MAX = 10.0

    personnelle = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name="soldes_permission"
    )
    annee = models.PositiveSmallIntegerField()
    solde_disponible = models.FloatField(default=SOLDE_MAX)
    date_reinitialisation = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Solde de permission"
        verbose_name_plural = "Soldes de permission"
        unique_together = ('personnelle', 'annee')
        ordering = ['-annee']

    def __str__(self):
        return f"Solde {self.annee} — {self.personnelle.nom} : {self.solde_disponible}j"

    def reinitialiser(self):
        from django.utils import timezone
        self.solde_disponible = self.SOLDE_MAX
        self.date_reinitialisation = timezone.now()
        self.save()


class Permissions(models.Model):
    STATUT_CHOICES = [
        ('En attente', 'En attente'),
        ('Approuvé', 'Approuvé'),
        ('Refusé', 'Refusé'),
    ]

    personnelle = models.ForeignKey(
        Personnelles,
        on_delete=models.CASCADE,
        related_name="permissions"
    )
    evenement = models.ForeignKey(
        EvenementPermission,
        on_delete=models.PROTECT,
        related_name="permissions",
        null=True,
        blank=True
    )
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    motif = models.TextField(blank=True)

    # Durée réelle accordée (auto depuis evenement, ou saisie RH pour evt 6 & 7)
    duree = models.FloatField(default=0)

    # Snapshot du solde avant/après approbation
    solde_initial = models.FloatField(default=0)
    solde_restant = models.FloatField(default=0)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='En attente'
    )
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        ordering = ['-date_creation']

    def __str__(self):
        return f"Permission — {self.personnelle.nom} ({self.date_debut.strftime('%d/%m/%Y')})"