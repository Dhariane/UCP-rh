from rest_framework import serializers
from api.models.fonction.modefinancement import ModeFinancement

class ModefinancementDto(serializers.ModelSerializer):
    class Meta:
        model = ModeFinancement
        fields=[
            "id",
            "nom"
        ]