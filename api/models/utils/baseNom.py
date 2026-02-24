from django.db import models
class BaseNom(models.Model):
    nom = models.CharField(
        max_length=100
    )
    class Meta:
        abstract = True