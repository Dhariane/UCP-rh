from django.db import models
from api.models.fonction.service import Services

class Fonctions(models.Model):
    nom = models.CharField()
    is_chef = models.BooleanField(default=False)
    service = models.ForeignKey(      
        Services,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fonctions'
    )

    def __str__(self):
        return f"{self.nom} "
