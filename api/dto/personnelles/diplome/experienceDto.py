from rest_framework import serializers
from api.models import Experience

class ExperienceDTO(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'id',
            'entreprise',
            'poste',
            'datedebut',
            'datefin',
            'description',
            'personnelle'
        ]