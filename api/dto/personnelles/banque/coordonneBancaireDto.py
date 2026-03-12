from rest_framework import serializers
from api.models.banque.coordonneesBancaires import CoordonneesBancaires
from api.models.banque.agences import Agences
from api.models.banque.banques import Banques
from django.db import models

class CoordonneesBancairesDto(serializers.ModelSerializer):
    class Meta:
        model = CoordonneesBancaires
        fields = ["id", "banque", "agence", "rib","photoRib","personnelle"]
