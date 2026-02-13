from rest_framework import serializers
from api.models.propos.personnelles import Personnelles
from api.models.propos.sexe import Sexes

class PersonnellesDTO(serializers.ModelSerializer):
    nom = serializers.CharField(),
    prenom = serializers.CharField()
    dateNaissance = serializers.DateField()  
    lieuNaissance = serializers.CharField()
    cin = serializers.IntegerField()
    propos = serializers.IntegerField()
    sexe = serializers.IntegerField()

    
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