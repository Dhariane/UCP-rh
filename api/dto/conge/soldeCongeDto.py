from rest_framework import serializers
from api.models.conge.soldeConge import SoldeConge

class SoldeCongeDto(serializers.ModelSerializer):
    class Meta:
        model = SoldeConge
        fields = ["id", "Personnelles","annee","total","reste"]