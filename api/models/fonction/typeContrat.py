from django.db import models
from api.models.propos.personnelles import Personnelles

class TypeContrats(models.Model):
    TypeContrat= models.CharField()
    