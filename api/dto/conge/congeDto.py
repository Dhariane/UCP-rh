from rest_framework import serializers
from api.models.conge.conge import Conge

class CongeDto(serializers.ModelSerializer):
    class Meta:
        model = Conge
        fields = ["id", "Personnel","typeConge","soldeConge","dateDebut","dateFin","nombreJours","description","statut"]