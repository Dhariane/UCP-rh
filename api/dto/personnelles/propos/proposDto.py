from rest_framework import serializers
from api.models.propos.propos import Propos
from api.models.propos.etatCivils import EtatCivil


class ProposDTO(serializers.ModelSerializer):
    etatCivil = serializers.PrimaryKeyRelatedField(
        queryset=EtatCivil.objects.all(),
        required=True
    )

    class Meta:
        model = Propos
        fields = [
            "id",
            "nif",
            "stat",
            "numeroCnaps",
            "tel",
            "email",
            "nombreEnfant",
            "etatCivil",
            "personnelle"
        ]

