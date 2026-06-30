from rest_framework import serializers
from api.models.conge.congePlanifieModel import CongePlanifie
from api.models.conge.typeConges import TypeConge


class TypeCongeShortDTO(serializers.ModelSerializer):
    class Meta:
        model  = TypeConge
        fields = ['id', 'libelle']


class CongePlanifieDTO(serializers.ModelSerializer):
    # Lecture : retourne { id, libelle } pour l'affichage front
    type_conge = TypeCongeShortDTO(read_only=True)

    class Meta:
        model  = CongePlanifie
        fields = [
            'id',
            'date_debut',
            'date_fin',
            'nombre_jours',
            'type_conge',
            'description',
            'created_at',
        ]