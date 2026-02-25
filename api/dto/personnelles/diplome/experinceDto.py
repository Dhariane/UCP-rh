from rest_framework import serializers
from api.models import Experience

class ExperienceDTO(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = [
            'id',
            'nombreExperience',
            'entreprise',
            'poste',
            'datedebut',
            'datefin',
            'description',
            'personnelle'
        ]