from rest_framework import serializers
from api.models.fonction.superieurs import Superieur
class SuperieurDto(serializers.ModelSerializer):
    class Meta:
        model = Superieur
        fields = ["id", "nom"]