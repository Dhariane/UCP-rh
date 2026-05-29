from rest_framework import serializers
from api.models.banque.banques import Banques


class BanqueDto(serializers.ModelSerializer):
    class Meta:
        model = Banques
        fields = ["id", "nom", "rib"]

