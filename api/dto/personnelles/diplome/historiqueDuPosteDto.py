from rest_framework import serializers
from api.models import HistoriqueDuPoste

class HistoriqueDuPosteDTO(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueDuPoste
        fields = [
            'id',
            'poste',
            'société',
            'datedebut',
            'datefin',
            'description',
            'personnelle'
        ]