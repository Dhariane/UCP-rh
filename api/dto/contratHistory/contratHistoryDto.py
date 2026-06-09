from rest_framework import serializers
from api.models.fonction.contrat import Contrat

class ContratHistorySerializer(serializers.ModelSerializer):
    # On récupère les noms au lieu des simples IDs pour faciliter l'affichage en Front
    fonction_nom = serializers.CharField(source='fonction.nom', read_only=True)
    service_nom = serializers.CharField(source='service.nom', read_only=True)
    type_contrat_nom = serializers.CharField(source='typeContrat.nom', read_only=True)
    financement_nom = serializers.CharField(source='financement.nom', read_only=True)

    class Meta:
        model = Contrat.history.model  # <-- On cible la table historique générée automatiquement
        fields = [
            'history_id', 'history_date', 'history_type', 
            'NumeroContrat', 'salaire', 'dateDebut', 'dateFin',
            'fonction_nom', 'service_nom', 'type_contrat_nom', 'financement_nom',
            'periodeEssai', 'is_actif'
        ]