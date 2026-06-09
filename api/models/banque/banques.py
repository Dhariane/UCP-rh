import api.models.utils.baseNom as baseNoms
from django.db import models


class Banques(baseNoms.BaseNom):
    rib = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.nom}"