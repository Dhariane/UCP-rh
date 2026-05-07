# api/dto/etat_civil_dto.py
from rest_framework import serializers
from api.models.propos.etatCivils import EtatCivil


class EtatCivilDTO(serializers.ModelSerializer):
    class Meta:
        model = EtatCivil
        fields = ["id", "nom"]
