from api.models.utils.baseNom import BaseNom
from api.models.utils.baseGrade import BaseGrades
from django.db import models
class Postes(BaseGrades,BaseNom):
    email = models.EmailField(
        max_length=100,
        null=True,
        blank=True,
        unique=True
    )
    tel = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    pass
def __str__(self):
    return self.nom
