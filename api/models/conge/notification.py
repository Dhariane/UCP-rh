from django.db import models
from django.utils import timezone
from api.models.auth.login.loginModel import Login
from api.models.conge.conge import Conge


class Notification(models.Model):
    """
    Notification générique envoyée à un utilisateur du système.
    Couvre toutes les étapes du workflow de validation de congé.
    """

    TYPE_CHOICES = [
        # Côté valideur : demande d'action
        ('validation_requise',    ' Validation requise'),
        ('remplacement_requis',   ' Validation par remplacement'),
        # Côté demandeur : retour du circuit
        ('conge_approuve',        'Congé approuvé'),
        ('conge_refuse',          ' Congé refusé'),
        ('conge_en_cours',        'Congé en cours de validation'),
        # Infos système
        ('rappel_validation',     ' Rappel de validation'),
        ('conge_annule',          ' Congé annulé'),
        ('rappel_conge', 'Rappel prise de congé'),
    ]

    destinataire   = models.ForeignKey(
        Login, on_delete=models.CASCADE,
        related_name='notifications'
    )
    conge          = models.ForeignKey(
        Conge, on_delete=models.CASCADE,
        related_name='notifications',
        null=True, blank=True
    )
    type_notif     = models.CharField(max_length=40, choices=TYPE_CHOICES)
    titre          = models.CharField(max_length=200)
    message        = models.TextField()
    lu             = models.BooleanField(default=False)
    date_creation  = models.DateTimeField(default=timezone.now)
    date_lecture   = models.DateTimeField(null=True, blank=True)
    # Données supplémentaires (étape, nom demandeur, etc.)
    metadata       = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-date_creation']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"[{self.type_notif}] → {self.destinataire} | {self.titre}"

    def marquer_lu(self):
        if not self.lu:
            self.lu = True
            self.date_lecture = timezone.now()
            self.save(update_fields=['lu', 'date_lecture'])