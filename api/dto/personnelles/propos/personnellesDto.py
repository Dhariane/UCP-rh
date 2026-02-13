from rest_framework import serializers
from api.models.propos.personnelles import Personnelles


class PersonnellesDTO(serializers.ModelSerializer):
    nom = serializers.CharField(),
    prenom = serializers.CharField()
    dateNaissance = serializers.DateField()  
    lieuNaissance = serializers.CharField()
    
    
    class Meta:
        model = Personnelles
        fields = [
            "id",
            "nom",
            "prenom",
            "dateNaissance",
            "lieuNaissance",
            "sexe",
            "propos",
            "cin"
        ]