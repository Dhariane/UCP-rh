from rest_framework import serializers
from api.models import Formation

class FormationDTO(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = [
            'id',
            'titre',
            'organisme',
            'lieu',
            'annee',
            'attestation',
            'personnelle'
        ]