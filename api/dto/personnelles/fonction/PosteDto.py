from rest_framework import serializers
from api.models.fonction.poste import Postes

class PosteDTO(serializers.ModelSerializer):
    class Meta:
        model = Postes
        fields = [
            "id",
            "nom",
            "grade",
            "email",
            "tel"
        ]