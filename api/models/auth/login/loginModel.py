from django.db import models

from api.models.propos.propos import Propos
from api.models.role.roleModel import Role
from api.models import Personnelles

class Login(models.Model):
    
    role = models.ForeignKey(
        Role, 
        on_delete=models.CASCADE, 
        related_name="logins"
    )
    
    email = models.ForeignKey(
        Propos, 
        to_field='email', # <--- POINTE SUR LE MAIL
        on_delete=models.CASCADE,
        related_name="logins"
    )
    personnelle = models.ForeignKey(
        Personnelles, 
        on_delete=models.CASCADE,
        null= True,
        blank=True,
        related_name="login")
    
    password = models.CharField(
        max_length=128,)
    
    created_at = models.DateTimeField(
        auto_now_add=True)
    
    def __str__(self):
        return f" Votre {self.email} et - {self.role} est bien enregistré"