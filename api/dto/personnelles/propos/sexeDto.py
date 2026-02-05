from rest_framework import serializers
from api.models.propos.sexe import Sexes
class SexeDTO(serializers.ModelSerializer):
    class Meta:
        model = Sexes
        fields = ["id", "nom"]