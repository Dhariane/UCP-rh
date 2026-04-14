from django.db import models

class TypeConge(models.Model):
    libelle = models.CharField(max_length=50)

    def __str__(self):
        return self.libelle