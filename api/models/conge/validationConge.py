from django.db import models
from api.models.conge.conge import Conge
from api.models.auth.login.loginModel import Login

class ValidationConge(models.Model):

    ETAPES = [
        ('chef',  'Chef direct'),
        ('gp', 'GP'),
        ('rf', 'RF'),
        ('cn', 'CN'),
        ('rh', 'RH'),
    ]

    DECISIONS = [
        ('approuve', 'Approuvé'),
        ('refuse',   'Refusé'),
    ]

    conge    = models.ForeignKey(
        Conge,
        on_delete=models.CASCADE,
        related_name='validations'
    )
    etape    = models.CharField(max_length=20, choices=ETAPES)
    decision = models.CharField(max_length=10, choices=DECISIONS)
    valideur = models.ForeignKey(
        Login,
        on_delete=models.SET_NULL,
        null=True,
        related_name='validations_effectuees'
    )
    motif    = models.TextField(blank=True, null=True)
    date     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.conge} → {self.etape} : {self.decision}"