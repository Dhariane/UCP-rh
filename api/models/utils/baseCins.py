from django.db import models

class BaseCins(models.Model):
    numeroCin = models.PositiveIntegerField(max_length=50, unique=True)
    dateCin = models.DateField()
    lieuCin = models.CharField(max_length=100)

    class Meta:
        abstract = True