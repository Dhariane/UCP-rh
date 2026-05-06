from rest_framework import serializers
from api.models.conge.passationservice import PassationService


class PassationServiceDTO(serializers.ModelSerializer):
    duree_absence = serializers.ReadOnlyField()  # propriété calculée

    class Meta:
        model = PassationService
        fields = [
            'id',
            'date_absence',
            'date_reprise',
            'date',
            'titulaire',
            'fonction',
            'statut',
            'remplacant',
            'duree_absence',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'duree_absence']