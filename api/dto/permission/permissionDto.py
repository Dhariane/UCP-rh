from rest_framework import serializers
from api.models.permission.permissionModel import EvenementPermission, Permissions, SoldePermission


class EvenementPermissionDto(serializers.ModelSerializer):
    class Meta:
        model = EvenementPermission
        fields = ['id', 'code', 'libelle', 'duree_defaut', 'est_fractionnable', 'delai_prise']


class SoldePermissionDto(serializers.ModelSerializer):
    personnelle_nom = serializers.CharField(source='personnelle.nom', read_only=True)

    class Meta:
        model = SoldePermission
        fields = ['id', 'personnelle', 'personnelle_nom', 'annee', 'solde_disponible', 'date_reinitialisation']
        read_only_fields = ['solde_disponible', 'date_reinitialisation']


class PermissionDto(serializers.ModelSerializer):
    # Événement
    evenement_libelle      = serializers.CharField(source='evenement.libelle', read_only=True)
    duree_defaut_evenement = serializers.FloatField(source='evenement.duree_defaut', read_only=True)

    # Infos employé
    nom_employe    = serializers.CharField(source='personnelle.nom', read_only=True)
    prenom_employe = serializers.CharField(source='personnelle.prenom', read_only=True)
    fonction       = serializers.SerializerMethodField()
    photoUrl       = serializers.SerializerMethodField()

    class Meta:
        model = Permissions
        fields = [
            'id',
            'personnelle',
            'nom_employe',
            'prenom_employe',
            'fonction',
            'photoUrl',
            'evenement',
            'evenement_libelle',
            'duree_defaut_evenement',
            'date_debut',
            'date_fin',
            'motif',
            'duree',
            'solde_initial',
            'solde_restant',
            'statut',
            'date_creation',
        ]
        read_only_fields = ['solde_initial', 'solde_restant', 'statut', 'date_creation']

    def get_fonction(self, obj):
        try:
            contrat = obj.personnelle.contrats.filter(
                date_fin__isnull=True
            ).select_related('fonction').first()
            if contrat and contrat.fonction:
                return contrat.fonction.nom
        except Exception:
            pass
        return None

    def get_photoUrl(self, obj):
        try:
            photo = obj.personnelle.photos.first()
            if photo and photo.data:
                return photo.data.url
        except Exception:
            pass
        return None