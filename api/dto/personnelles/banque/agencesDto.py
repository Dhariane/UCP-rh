from rest_framework import serializers
from api.models.banque.agences import Agences

class AgenceDto(serializers.ModelSerializer):
    class Meta:
        model = Agences
        fields = ["id", "nom","ville"]