from rest_framework import serializers
from api.models.propos.Cins import Cins

class CinsDTO(serializers.ModelSerializer):
    dateCin = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d", "%d/%m/%Y"])
    dateDuplicata = serializers.DateField(input_formats=['%Y-%m-%d', '%d/%m/%Y'], required=False, allow_null=True)
    numeroCin = serializers.CharField()
    class Meta:
        model = Cins
        fields = [
            "id",
            "numeroCin",
            "dateCin",
            "lieuCin",
            "numeroDuplicata",
            "dateDuplicata",
            "lieuDuplicata",
            "personnelle",
        ]