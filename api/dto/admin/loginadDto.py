from rest_framework import serializers
from api.models.admin.loginadModel import Loginadmin
from django.contrib.auth.hashers import make_password

class LoginadminDTO(serializers.ModelSerializer):
    # Puisque ton modèle Loginadmin a un champ email direct (EmailField)
    # On garde une structure cohérente avec tes autres DTOs
    
    role_name = serializers.CharField(source='role.name', read_only=True)

    class Meta:
        model = Loginadmin
        fields = [
            'id', 
            'email', 
            'role', 
            'role_name',
            'password', 
            'created_at'
        ]
        
        extra_kwargs = {
            'role': {'required': True}, # Un admin doit généralement avoir un rôle
            'password': {
                'write_only': True,     # Jamais renvoyé dans les réponses API
                'required': True
            }
        }

    def create(self, validated_data):
        """
        Logique personnalisée pour hacher le mot de passe à la création
        """
        # On récupère le mot de passe brut et on le hache avant sauvegarde
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        return super().create(validated_data)