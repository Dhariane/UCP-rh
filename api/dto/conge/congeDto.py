from rest_framework import serializers
from api.models.conge.conge import Conge
from api.models.propos.personnelles import Personnelles
from api.models.conge.typeConges import TypeConge
from api.models.conge.soldeConge import SoldeConge
from api.models.conge.statut import Statut


class CongeDTO(serializers.ModelSerializer):
    # ForeignKeys avec PrimaryKeyRelatedField
    personnel = serializers.PrimaryKeyRelatedField(queryset=Personnelles.objects.all())
    type_conge = serializers.PrimaryKeyRelatedField(queryset=TypeConge.objects.all())
    solde_conge = serializers.PrimaryKeyRelatedField(queryset=SoldeConge.objects.all())
    statut = serializers.PrimaryKeyRelatedField(queryset=Statut.objects.all())
    
    # Champ calculé (lecture seule)
    nombre_jours = serializers.IntegerField(read_only=True)
    
    # Utilisateur qui valide (optionnel)
    # validated_by = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), 
    #     required=False, 
    #     allow_null=True
    # )

    class Meta:
        model = Conge
        fields = [
            'id',
            'personnel',
            'type_conge',
            'solde_conge',
            'date_debut',
            'date_fin',
            'nombre_jours',
            'description',
            'statut',
            'validated_by',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['nombre_jours', 'created_at', 'updated_at']