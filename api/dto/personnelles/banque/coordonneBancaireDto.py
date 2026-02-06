from rest_framework import serializers
from api.models.banque.coordonneesBancaires import CoordonneesBancaires
from api.models.banque.agences import Agences
from api.models.banque.banques import Banques

class CoordonneesBancairesDto(serializers.ModelSerializer):
    agence = serializers.PrimaryKeyRelatedField(queryset=Agences.objects.all())
    banque = serializers.PrimaryKeyRelatedField(queryset=Banques.objects.all())
    class Meta:
        model = CoordonneesBancaires
        fields = ["id", "rib", "banque", "agence"]