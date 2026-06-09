from django.db import models

class TypeConge(models.Model):
    libelle = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, blank=True, null=True)  # ex: ANN, MAL, etc.
    duree_max = models.PositiveIntegerField(null=True, blank=True)  # jours max autorisés

    class Meta:
        verbose_name = "Type de congé"
        verbose_name_plural = "Types de congé"

    def __str__(self):
        return self.libelle