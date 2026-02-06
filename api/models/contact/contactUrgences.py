from django.db import models
from api.models.utils.baseNom import BaseNom
from api.models.propos.personnelles import Personnelles
from api.models.contact.relation import Relations
class ContactUrgences(BaseNom):
    telephone= models.CharField(max_length=30)
    adresse = models.CharField(max_length=100)
    personnelle = models.ForeignKey(Personnelles, on_delete=models.PROTECT,related_name="contactUrgence")
    relation = models.ForeignKey(Relations,on_delete=models.PROTECT,related_name="contactUrgent")

    def __str__(self):
        return f"{(self.nom)}"