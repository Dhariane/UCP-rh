from rest_framework import serializers
from api.models.fonction.typeContrat import TypeContrats

class TypeContratDto(serializers.ModelSerializer):
    class Meta:
        model = TypeContrats
        fields = [
            "id",
            "TypeContrat",
        ]
