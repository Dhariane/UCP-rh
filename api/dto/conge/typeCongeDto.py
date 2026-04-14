from rest_framework import serializers
from api.models.conge.typeConges import TypeConge

class TypeCongeDto(serializers.ModelSerializer):
    class Meta:
        model = TypeConge
        fields = ["id", "libelle"]