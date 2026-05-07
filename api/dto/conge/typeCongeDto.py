from rest_framework import serializers
from api.models.conge.typeConges import TypeConge

class TypeCongeDTO(serializers.ModelSerializer):
    class Meta:
        model = TypeConge
        fields = ['id', 'libelle', 'code', 'duree_max']