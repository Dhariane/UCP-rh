from django.db import models
from django.core.exceptions import ValidationError
from api.models.propos.personnelles import Personnelles
from .typeConges import TypeConge
from .statut import Statut
from .soldeConge import SoldeConge
from .passationservice import PassationService

class Conge(models.Model):
    ETAPES = [
                ('passation', 'En attente remplaçant'),
                ('chef',    'En attente chef'),
                ('gp_pf',   'En attente GP/PF'),
                ('cn',      'En attente CN'),
                ('rh',      'En attente RH'),
                ('termine', 'Terminé'),
        ]
    
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
        'api.Login',  # ton modèle custom
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conges_validated'
    )
    passation_service = models.ForeignKey(
        PassationService,          
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conges_passation'
    )
    # ✅ AJOUTER JUSTE CE CHAMP
    etape_validation = models.CharField(
        max_length=20,
        choices=ETAPES,
        default='passation',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['-created_at']

    # 🔥 VALIDATION
    def clean(self):
        if self.date_debut and self.date_fin:
            if self.date_fin < self.date_debut:
                raise ValidationError("Date de fin invalide")

            self.nombre_jours = (self.date_fin - self.date_debut).days + 1

            # ✅ Vérifier le solde UNIQUEMENT à la création
            if not self.pk:
                if self.solde_conge.reste - self.nombre_jours < 10:
                    raise ValidationError(
                        "Vous devez garder au moins 10 jours de solde après ce congé"
                    )
                if self.nombre_jours > self.solde_conge.reste:
                    raise ValidationError("Solde insuffisant")

    def save(self, *args, **kwargs):
        # ✅ Recalculer nombre_jours sans bloquer si c'est une mise à jour
        if self.date_debut and self.date_fin:
            self.nombre_jours = (self.date_fin - self.date_debut).days + 1

        if not self.pk:
            if self.nombre_jours == 1:
                self.etape_validation = 'chef'
            else:
                self.etape_validation = 'passation'

        old_statut_id = None
        if self.pk:
            old = Conge.objects.get(pk=self.pk)
            old_statut_id = old.statut_id

        super().save(*args, **kwargs)

        solde = self.solde_conge

        if self.statut_id == 2:
            if old_statut_id != 2:
                solde.utilise += self.nombre_jours

        if self.statut_id == 3:
            if old_statut_id == 2:
                solde.utilise -= self.nombre_jours

        if solde.utilise < 0:
            solde.utilise = 0

        solde.save()