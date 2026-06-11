from rest_framework import serializers
from api.models.fonction.fonctions import Fonctions
class FonctionDto(serializers.ModelSerializer):
    class Meta:
        model = Fonctions
        fields = [
            "id",
            "nom",
<<<<<<< HEAD
=======
            "dateDebut",
            "dateFin",
            "personnelle",
            "service",
            "poste",
            "financement"
>>>>>>> 23088e43 (mon enregistrement local)
        ]