from django.db import models

class Role(models.Model):
    # Le nom du rôle (ex: Admin, Editeur, Utilisateur)
    name = models.CharField(
        max_length=100, 
        unique=True
    )
    
    # Date et heure de création automatique
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Role {self.name} créé le {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"