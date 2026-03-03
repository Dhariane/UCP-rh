from rest_framework import serializers
from api.models.role.roleModel import Role # Adapte le chemin selon ton dossier

class RoleDTO(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'created_at']
        read_only_fields = ['created_at']