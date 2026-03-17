from rest_framework import serializers
from api.models import *

# --- 1. TABLES DE RÉFÉRENCE (Listes déroulantes) ---
class SexeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sexes
        fields = ['id', 'nom']

class EtatCivilSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtatCivil
        fields = ['id', 'nom']

class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relations
        fields = ['id', 'nom']

class TypeContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeContrats
        fields = ['id', 'TypeContrat']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'nom']

class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postes
        fields = ['id', 'nom']

class ModeFinancementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeFinancement
        fields = ['id', 'nom']

# --- 2. TABLES LIÉES AU CONTRAT ET À LA FONCTION ---
class ContratSerializer(serializers.ModelSerializer):
    typeContrat = TypeContratSerializer(read_only=True)
    class Meta:
        model = Contrat
        fields = ['id', 'NumeroContrat', 'photoContrat', 'typeContrat']

class FonctionSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    poste = PosteSerializer(read_only=True)
    financement = ModeFinancementSerializer(read_only=True)
    class Meta:
        model = Fonctions
        fields = ['id', 'nom', 'dateDebut', 'dateFin', 'service', 'poste', 'financement']

# --- 3. TABLES DE DÉTAILS PERSONNELS ---
class CinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cins
        fields = '__all__'

class CoordonneesBancaireSerializer(serializers.ModelSerializer):
    banque_nom = serializers.CharField(source='banque.nom', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom', read_only=True)
    class Meta:
        model = CoordonneesBancaires
        fields = ['id', 'rib', 'photoRib', 'banque_nom', 'agence_nom']

class ProposSerializer(serializers.ModelSerializer):
    etatCivil = EtatCivilSerializer(read_only=True)
    # On récupère les coordonnées bancaires liées au propos
    coordonnees = CoordonneesBancaireSerializer(source='coordonneesbancaire', read_only=True)
    class Meta:
        model = Propos
        fields = '__all__'

# --- 4. LISTES (DIPLÔMES, ENFANTS, EXPÉRIENCES) ---
class DiplomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diplome
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class EnfantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfant
        fields = '__all__'


# --- 5. LE SERIALIZER GLOBAL : PersonnelFullSerializer ---
class PersonnelFullSerializer(serializers.ModelSerializer):
    sexe = SexeSerializer(read_only=True)
    cins = CinSerializer(many=True, read_only=True)
    propos = ProposSerializer(source='propos_list', many=True, read_only=True)
    
    # Relations contractuelles
    # 'contrat' et 'fonctions' doivent être les related_name dans tes modèles
    contrats = ContratSerializer(many=True, read_only=True, source='contrat')
    fonctions = FonctionSerializer(many=True, read_only=True)
    coordonnees = CoordonneesBancaireSerializer(source='coordonnees_bancaires', read_only=True)
    
    # Listes diverses
    diplomes = DiplomeSerializer(many=True, read_only=True, source='Diplome') 
    experiences = ExperienceSerializer(many=True, read_only=True, source='Experience')
    enfants = EnfantSerializer(many=True, read_only=True, source='Enfant')
    
    class Meta:
        model = Personnelles
        fields = '__all__'
        depth = 1 # Sécurité pour récupérer les FK simples