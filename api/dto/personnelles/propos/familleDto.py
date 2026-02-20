from rest_framework import serializers
from api.models.propos.famille import Famille
from api.models.propos.personnelles import Personnelles

class FamilleDto(serializers.ModelSerializer):
    personnelle = serializers.PrimaryKeyRelatedField(
        queryset=Personnelles.objects.all(),
        required=True
    )

    class Meta:
        model = Famille
        fields = [
            "id",
            "nomPere",
            "prenomPere",
            "nomMere",
            "prenomMere",
            "nomConjoint",
            "prenomConjoint",
            "nombreEnfant",
            "personnelle"
        ]