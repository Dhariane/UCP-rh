from rest_framework import serializers
from api.models.banque.banques import Banques

<<<<<<< HEAD

class BanqueDto(serializers.ModelSerializer):
    class Meta:
        model = Banques
        fields = ["id", "nom", "rib"]
=======
class BanqueDto(serializers.ModelSerializer):
    class Meta:
        model = Banques
        fields = ["id", "nom"]
>>>>>>> 23088e43 (mon enregistrement local)
