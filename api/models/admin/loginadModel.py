from django.db import models
from api.models.role.roleModel import Role

class Loginadmin(models.Model):
    
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE, 
        related_name="admin_login"
    )
    
    email = models.EmailField(
        max_length=100,
        null=False,
        blank=True,
        unique=True
    )
    
    password = models.CharField(
        max_length=128,)
    
    created_at = models.DateTimeField(
        auto_now_add=True)
    
    def __str__(self):
        return f" Votre {self.email} et - {self.role} est bien enregistré"