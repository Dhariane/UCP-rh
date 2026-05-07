from django.db import models
from api.models.utils.baseNom import BaseNom

class Agences(BaseNom,models.Model):
    ville= models.CharField(
        max_length=100
    )
    pass
    def __str__(self):
        return f"{(self.nom)}"