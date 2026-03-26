from rest_framework import serializers
from api.models.propos.personnelles import Personnelles
from api.models.propos.sexe import Sexes
from api.models.propos.propos import Propos
from api.models.propos.Cins import Cins

class PersonnellesDTO(serializers.ModelSerializer):
    # Champs normaux
    nom = serializers.CharField()
    prenom = serializers.CharField()
    dateNaissance = serializers.DateField()
    lieuNaissance = serializers.CharField()
    
    # Champs ForeignKey avec ID
    sexe = serializers.PrimaryKeyRelatedField(queryset=Sexes.objects.all())
    propos = serializers.PrimaryKeyRelatedField(queryset=Propos.objects.all(),required=False)
    cin = serializers.PrimaryKeyRelatedField(queryset=Cins.objects.all(),required=False)
    
    class Meta:
        model = Personnelles
        fields = [
            "id",
            "nom",
            "prenom",
            "dateNaissance",
            "lieuNaissance",
            "adresse",
            "quartier",
            "ville",
            "sexe",
            "propos",
            "cin",
            "photoResidence",
            "acteNaissance",
            "casierjudiciaire",
            "cinphoto",
            "telPerso",
            "emailPerso"
        ]
