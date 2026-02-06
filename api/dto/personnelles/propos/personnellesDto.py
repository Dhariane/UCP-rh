from rest_framework import serializers
from api.models.propos.personnelles import Personnelles
from api.models.propos.sexe import Sexes

class PersonnellesDTO(serializers.ModelSerializer):
    sexe = serializers.PrimaryKeyRelatedField(
        queryset=Sexes.objects.all(),
        required=True   
    )
    class Meta:
        model = Personnelles
        fields = [
            "id",
            "nom",
            "prenom",
            "dateNaissance",
            "lieuNaissance",
            "sexe",
        ]