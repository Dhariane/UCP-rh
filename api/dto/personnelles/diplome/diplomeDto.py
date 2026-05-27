<<<<<<< HEAD
from rest_framework import serializers
from api.models import Diplome

class DiplomeDTO(serializers.ModelSerializer):
    class Meta:
        model = Diplome
        fields = [
            'id',
            'nom',
            'etablissement',
            'dateObtention',
            'photo',
            'personnelle'
=======
from rest_framework import serializers
from api.models import Diplome

class DiplomeDTO(serializers.ModelSerializer):
    class Meta:
        model = Diplome
        fields = [
            'id',
            'nom',
            'etablissement',
            'anneeObtention',
            'photo',
            'lieu',
            'filiere',
            'type_diplome',
            'personnelle'
>>>>>>> 5672fea1 (modif pas encore terminée)
        ]