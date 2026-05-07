from api.models.utils.baseCins import BaseCins
from django.db import models
class Cins(BaseCins):
    personnelle = models.ForeignKey(
        'Personnelles', 
        on_delete=models.CASCADE,
        related_name='cins'
    )
    pass