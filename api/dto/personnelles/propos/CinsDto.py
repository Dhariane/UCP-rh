from rest_framework import serializers
from api.models.propos.Cins import Cins

class CinsDTO(serializers.ModelSerializer):
    class Meta:
        model = Cins
        fields = [
            "id",
            "numeroCin",
            "dateCin",
            "lieuCin",
            "personnelle"
        ]