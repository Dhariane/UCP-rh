from django.db import models

class BaseCins(models.Model):
    numeroCin = models.CharField(unique=True,max_length=12)
    dateCin = models.DateField()
    lieuCin = models.CharField(max_length=100)

    class Meta:
        abstract = True