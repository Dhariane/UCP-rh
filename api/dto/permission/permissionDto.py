from rest_framework import serializers
from api.models.propos.personnelles import Personnelles
from api.models.permission.permissionModel import Permissions

class PermissionDto(serializers.ModelSerializer):
    # On ajoute ces champs pour que le Dashboard Next.js affiche le nom sans refaire de fetch
    nom_employe = serializers.ReadOnlyField(source='personnelle.nom')
    prenom_employe = serializers.ReadOnlyField(source='personnelle.prenom')

    class Meta:
        model = Permissions
        fields = [
            'id', 'personnelle', 'nom_employe', 'prenom_employe', 
            'date_debut', 'date_fin', 'motif', 'statut', 'date_creation'
        ] 