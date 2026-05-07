from rest_framework import serializers
from api.models.conge.statut import Statut

class StatutDto(serializers.ModelSerializer):
    class Meta:
        model = Statut
        fields = ["id", "statut"]