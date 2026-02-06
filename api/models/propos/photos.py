from django.db import models
from api.models.utils.baseNom import BaseNom
from api.models.propos.personnelles import Personnelles

class Photos(BaseNom):
    data = models.ImageField(upload_to='photos/')
    personnelle = models.ForeignKey(Personnelles, on_delete=models.PROTECT, related_name="photos")

    def __str__(self):
        return f"{(self.data)}"