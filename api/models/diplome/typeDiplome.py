from django.db import models

class DiplomeType(models.Model):
    nom = models.CharField(max_length=150, unique=True)
        
    class Meta:
        verbose_name = "Type de diplôme"
        verbose_name_plural = "Types de diplômes"
        ordering = ['nom']

    def __str__(self):
        return self.nom
    
   