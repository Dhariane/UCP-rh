from rest_framework import serializers
from api.models.fonction.contrat import Contrat

class ContratDto(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields = [
            "id",
            "NumeroContrat",
            "photoContrat",
            "typeContrat",
            "personnelle",
        ]
