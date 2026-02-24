from rest_framework import serializers
from api.models import Diplome

class DiplomeDTO(serializers.ModelSerializer):
    class Meta:
        model = Diplome
        fields = [
            'id',
            'nom',
            'etablissement',
            'dateObtention',
            'photo',
            'personnelle'
        ]