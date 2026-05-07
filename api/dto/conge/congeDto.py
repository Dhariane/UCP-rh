<<<<<<< HEAD
from rest_framework import serializers
from api.models.conge.conge import Conge
from api.models.propos.personnelles import Personnelles
from api.models.conge.typeConges import TypeConge
from api.models.conge.soldeConge import SoldeConge
from api.models.conge.statut import Statut
from api.models.conge.passationservice import PassationService  # ← ajouter cet import


class CongeDTO(serializers.ModelSerializer):
    personnel = serializers.PrimaryKeyRelatedField(queryset=Personnelles.objects.all())
    type_conge = serializers.PrimaryKeyRelatedField(queryset=TypeConge.objects.all())
    solde_conge = serializers.PrimaryKeyRelatedField(queryset=SoldeConge.objects.all())
    statut = serializers.PrimaryKeyRelatedField(queryset=Statut.objects.all())
    nombre_jours = serializers.IntegerField(read_only=True)

    # ✅ AJOUTER CECI
    passation_service = serializers.PrimaryKeyRelatedField(
        queryset=PassationService.objects.all(),
        required=False,
        allow_null=True
    )
    statut       = serializers.PrimaryKeyRelatedField(
        queryset=Statut.objects.all(),
        required=False,    # ← plus obligatoire
        allow_null=True    # ← peut être null
    )

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
            'passation_service',
            'validated_by',
            'created_at',
            'updated_at'
        ]
=======
from rest_framework import serializers
from api.models.conge.conge import Conge
from api.models.propos.personnelles import Personnelles
from api.models.conge.typeConges import TypeConge
from api.models.conge.soldeConge import SoldeConge
from api.models.conge.statut import Statut
from api.models.conge.passationservice import PassationService  # ← ajouter cet import


class CongeDTO(serializers.ModelSerializer):
    personnel = serializers.PrimaryKeyRelatedField(queryset=Personnelles.objects.all())
    type_conge = serializers.PrimaryKeyRelatedField(queryset=TypeConge.objects.all())
    solde_conge = serializers.PrimaryKeyRelatedField(queryset=SoldeConge.objects.all())
    statut = serializers.PrimaryKeyRelatedField(queryset=Statut.objects.all())
    nombre_jours = serializers.IntegerField(read_only=True)

    # ✅ AJOUTER CECI
    passation_service = serializers.PrimaryKeyRelatedField(
        queryset=PassationService.objects.all(),
        required=False,
        allow_null=True
    )

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
            'passation_service',
            'validated_by',
            'created_at',
            'updated_at'
        ]
>>>>>>> 23088e43 (mon enregistrement local)
        read_only_fields = ['nombre_jours', 'created_at', 'updated_at']