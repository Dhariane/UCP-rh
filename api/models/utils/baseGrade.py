from django.db import models
from api.models.utils.baseNom import BaseNom
class BaseGrades(BaseNom):
    grade = models.IntegerField()
    class Meta:
        abstract = True