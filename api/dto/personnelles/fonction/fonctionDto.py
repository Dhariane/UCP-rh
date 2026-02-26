from rest_framework import serializers
from api.models.fonction.fonctions import Fonctions
class FonctionDto(serializers.ModelSerializer):
    class Meta:
        model = Fonctions
        fields = [
            "id",
            "nom",
            "dateDebut",
            "dateFin",
            "financement",
            "personnelle",
            "service",
            "poste",
            "superieur"
        ]