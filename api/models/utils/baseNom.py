from django.db import models
class BaseNom(models.Model):
    nom = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    
    class Meta:
        abstract = True