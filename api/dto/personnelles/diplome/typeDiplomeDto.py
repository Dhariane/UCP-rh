from rest_framework import serializers
from api.models import DiplomeType

class TypeDiplomeDTO(serializers.ModelSerializer):
    class Meta:
        model = DiplomeType
        fields = [
            'id',
            'nom',
        ]