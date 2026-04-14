from django.db import models


class Statut(models.Model):
    statut = models.CharField()

    def __str__(self):
        return self.statut