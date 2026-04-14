from rest_framework import serializers
from api.models.auth.login.loginModel import Login

class LoginDTO(serializers.ModelSerializer):
    # On peut afficher l'email directement au lieu de l'ID de la personne
    email_detail = serializers.EmailField(source='email.email', read_only=True)
    personnel_id = serializers.IntegerField(source='email.id', read_only=True)
    
    class Meta:
        model = Login
        fields = [
            'id', 
            'email',         # Accepte l'email (ForeignKey vers Propos)
            'email_detail',  # Pour l'affichage clair en lecture
            'personnel_id',
            'role', 
            'password', 
            'created_at',
            'personnelles'
        ]
        
        extra_kwargs = {
            'role': {'required': False, 'allow_null': True},
            'password': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        """
        Logique personnalisée pour hacher le mot de passe à la création
        """
        from django.contrib.auth.hashers import make_password
        
        # On récupère le mot de passe brut et on le hache avant sauvegarde
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)