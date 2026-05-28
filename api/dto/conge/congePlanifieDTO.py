from rest_framework import serializers
from api.models.conge.congePlanifieModel import CongePlanifie
# Ajuste le chemin ci-dessous selon l'emplacement de ton TypeConge
from api.models.conge.typeConges import TypeConge

class TypeCongeShortDTO(serializers.ModelSerializer):
    class Meta:
        model = TypeConge
        fields = ['id', 'libelle']

class CongePlanifieDTO(serializers.ModelSerializer):
    # Imbrique le DTO court pour renvoyer l'objet {id, libelle} attendu par le front
    type_conge = TypeCongeShortDTO(read_only=True)

    class Meta:
        model = CongePlanifie
        fields = ['id', 'date_debut', 'date_fin', 'nombre_jours', 'type_conge', 'description']