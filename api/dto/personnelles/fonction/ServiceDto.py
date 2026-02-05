from rest_framework import serializers
from api.models.fonction.service import Services 
class ServiceDto(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ["id", "nom"]