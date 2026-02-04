from api.models.utils.baseNom import BaseNom
from django.db import models
class Test(BaseNom):
    sexe = models.CharField(max_length=10)