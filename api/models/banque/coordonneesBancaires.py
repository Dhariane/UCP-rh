from django.db import models
from api.models.banque.banques import Banques
from api.models.banque.agences import Agences

class CoordonneesBancaires(models.Model):
    rib = models.CharField(max_length=100)
    banque = models.ForeignKey(Banques, on_delete=models.PROTECT, related_name="coordonneesBancaires")
    agence = models.ForeignKey(Agences, on_delete=models.PROTECT, related_name="coordonneesBancaires")
    # Ajout du champ photo
    photoRib = models.ImageField(upload_to='ribs/', null=True, blank=True)

    def __str__(self):
        return f"{self.rib}"