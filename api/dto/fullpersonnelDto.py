from decimal import Decimal
import json
from urllib.parse import urlparse, unquote

from rest_framework import serializers
from api.models import *
from api.services.personnelles.diplome.experienceService import ExperienceService
from api.services.personnelles.fonction import ServiceService
from api.services.personnelles.fonction.fonctionService import FonctionService
from api.services.personnelles.propos.enfantService import EnfantService

# ==========================================
# HELPER GLOBAL (hors de toute classe)
# ==========================================

def clean_file_url(file_field):
    """Convertit n'importe quel FileField en URL propre /media/xxx"""
    if not file_field:
        return None
    try:
        name = file_field.name
        if not name:
            return None
        # Cas corrompu : URL absolue ou encodée stockée en DB
        if 'http' in name or '%' in name:
            decoded = unquote(name)
            parsed = urlparse(decoded)
            return f"http://127.0.0.1:8000{parsed.path}"
        # Cas normal : chemin relatif → .url retourne /media/xxx
        return file_field.url
    except Exception:
        return None


# ==========================================
# 1. SERIALIZERS DE RÉFÉRENCE
# ==========================================

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


# ==========================================
# 2. SERIALIZERS DES TABLES LIÉES
# ==========================================

class EnfantSerializer(serializers.ModelSerializer):
    certificatVie = serializers.SerializerMethodField()

    def get_certificatVie(self, obj):
        return clean_file_url(obj.certificatVie)

    class Meta:
        model = Enfant
        fields = '__all__'


class ContactUrgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUrgences
        fields = ['id', 'nom', 'telephone', 'adresse', 'relation']


class DiplomeSerializer(serializers.ModelSerializer):
    # Le champ s'appelle "photo" dans le modèle Diplome
    # On l'expose sous le nom "fichier" pour le frontend
    fichier = serializers.SerializerMethodField()

    def get_fichier(self, obj):
        return clean_file_url(getattr(obj, 'photo', None))

    class Meta:
        model = Diplome
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class FormationSerializer(serializers.ModelSerializer):
    # Le champ s'appelle "attestation" dans le modèle Formation
    # On l'expose sous le nom "certificat" pour le frontend
    certificat = serializers.SerializerMethodField()

    def get_certificat(self, obj):
        return clean_file_url(getattr(obj, 'attestation', None))

    class Meta:
        model = Formation
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ['id', 'nom']

class ModeFinancementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeFinancement
        fields = ['id', 'nom']

class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postes
        fields = ['id', 'nom']

class TypeContratSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeContrats
        fields = ['id', 'nom']


# ==========================================
# 3. SERIALIZER DE LECTURE (GET FULL)
# ==========================================

class PersonnelFullSerializer(serializers.ModelSerializer):
    # --- Alias et Relations ---
    emailPersonnel     = serializers.CharField(source='emailPerso', default="")
    telephonePersonnel = serializers.CharField(source='telPerso', default="")
    contactsUrgence    = ContactUrgenceSerializer(many=True, read_only=True, source='contactUrgence')
    diplomes           = DiplomeSerializer(many=True, read_only=True, source='Diplome')
    experiences        = ExperienceSerializer(many=True, read_only=True, source='Experience')
    formations         = FormationSerializer(many=True, read_only=True, source='Formation')
    enfants            = EnfantSerializer(many=True, read_only=True, source='Enfant')

    # --- Champs SerializerMethodField ---
    cin                  = serializers.SerializerMethodField()
    dateDelivranceCin    = serializers.SerializerMethodField()
    lieuDelivranceCin    = serializers.SerializerMethodField()
    nomPere              = serializers.SerializerMethodField()
    nomMere              = serializers.SerializerMethodField()
    rib                  = serializers.SerializerMethodField()
    banque               = serializers.SerializerMethodField()
    agence               = serializers.SerializerMethodField()
    photoRib             = serializers.SerializerMethodField()
    conjoint             = serializers.SerializerMethodField()
    photoUrl             = serializers.SerializerMethodField()
    contrat              = serializers.SerializerMethodField()
    date_embauche        = serializers.SerializerMethodField()
    date_sortie          = serializers.SerializerMethodField()
    financement_actuel   = serializers.SerializerMethodField()
    service_actuel       = serializers.SerializerMethodField()
    poste_superieur      = serializers.SerializerMethodField()
    fonction             = serializers.SerializerMethodField()
    villeAgence          = serializers.SerializerMethodField()
    nif                  = serializers.SerializerMethodField()
    stat                 = serializers.SerializerMethodField()
    cnaps                = serializers.SerializerMethodField()
    emailProfessionnel   = serializers.SerializerMethodField()
    contactProfessionnel = serializers.SerializerMethodField()
    etatCivil            = serializers.SerializerMethodField()
    nombreEnfants        = serializers.SerializerMethodField()

    # Champs fichiers directs sur Personnelles → URL propre
    photoResidence   = serializers.SerializerMethodField()
    cinphoto         = serializers.SerializerMethodField()
    acteNaissance    = serializers.SerializerMethodField()
    casierjudiciaire = serializers.SerializerMethodField()

    class Meta:
        model = Personnelles
        fields = [
            'id', 'nom', 'prenom', 'sexe', 'dateNaissance', 'lieuNaissance', 'adresse',
            'emailPersonnel', 'telephonePersonnel', 'photoUrl', 'quartier', 'ville',
            'cin', 'date_embauche', 'fonction', 'date_sortie', 'poste_superieur',
            'service_actuel', 'financement_actuel',
            'contrat', 'dateDelivranceCin', 'lieuDelivranceCin',
            'etatCivil', 'nombreEnfants', 'conjoint',
            'nomPere', 'nomMere',
            'emailProfessionnel', 'contactProfessionnel', 'nif', 'stat', 'cnaps',
            'rib', 'banque', 'agence', 'villeAgence', 'photoRib',
            'enfants', 'contactsUrgence', 'diplomes', 'experiences', 'formations',
            'photoResidence', 'cinphoto', 'acteNaissance', 'casierjudiciaire',
        ]

    # ── Cache ──────────────────────────────────────────────
    def _get_related_data(self, obj):
        if not hasattr(self, '_cached_dict'):
            self._cached_dict = {}
        if obj.id not in self._cached_dict:
            self._cached_dict[obj.id] = {
                'fonction': Fonctions.objects.filter(personnelle=obj).last(),
                'propos':   Propos.objects.filter(personnelle=obj).last(),
                'famille':  Famille.objects.filter(personnelle=obj).first(),
                'banque':   CoordonneesBancaires.objects.filter(personnelle=obj).first(),
                'cin':      obj.cins.first(),
            }
        return self._cached_dict[obj.id]

    # ── Fichiers directs sur Personnelles ──────────────────
    def get_photoResidence(self, obj):
        return clean_file_url(obj.photoResidence)

    def get_cinphoto(self, obj):
        return clean_file_url(obj.cinphoto)

    def get_acteNaissance(self, obj):
        return clean_file_url(obj.acteNaissance)

    def get_casierjudiciaire(self, obj):
        return clean_file_url(obj.casierjudiciaire)

    # ── Photo profil ───────────────────────────────────────
    def get_photoUrl(self, obj):
        p = obj.photos.first()
        if p and p.data:
            try:
                return p.data.url
            except Exception:
                return None
        return None

    # ── Fonction ───────────────────────────────────────────
    def get_fonction(self, obj):
        f = self._get_related_data(obj)['fonction']
        return f.nom if f else ""

    def get_date_embauche(self, obj):
        f = self._get_related_data(obj)['fonction']
        return str(f.dateDebut) if f and f.dateDebut else None

    def get_date_sortie(self, obj):
        f = self._get_related_data(obj)['fonction']
        return str(f.dateFin) if f and f.dateFin else None

    def get_financement_actuel(self, obj):
        f = self._get_related_data(obj)['fonction']
        return f.financement.nom if f and f.financement else "Non défini"

    def get_service_actuel(self, obj):
        f = self._get_related_data(obj)['fonction']
        return f.service.nom if f and f.service else "Non défini"

    def get_poste_superieur(self, obj):
        f = self._get_related_data(obj)['fonction']
        return f.poste.nom if f and f.poste else "Non défini"

    # ── Propos ─────────────────────────────────────────────
    def get_nif(self, obj):
        p = self._get_related_data(obj)['propos']
        return p.nif if p else ""

    def get_stat(self, obj):
        p = self._get_related_data(obj)['propos']
        return p.stat if p else ""

    def get_cnaps(self, obj):
        p = self._get_related_data(obj)['propos']
        return p.numeroCnaps if p else ""

    def get_emailProfessionnel(self, obj):
        p = self._get_related_data(obj)['propos']
        return p.email if p else ""

    def get_contactProfessionnel(self, obj):
        p = self._get_related_data(obj)['propos']
        return p.tel if p else ""

    def get_etatCivil(self, obj):
        p = self._get_related_data(obj)['propos']
        return p.etatCivil.id if p and p.etatCivil else None

    def get_nombreEnfants(self, obj):
        p = self._get_related_data(obj)['propos']
        return p.nombreEnfant if p else 0

    # ── Famille ────────────────────────────────────────────
    def get_nomPere(self, obj):
        fam = self._get_related_data(obj)['famille']
        return fam.nomPere if fam else ""

    def get_nomMere(self, obj):
        fam = self._get_related_data(obj)['famille']
        return fam.nomMere if fam else ""

    def get_conjoint(self, obj):
        fam = self._get_related_data(obj)['famille']
        if fam:
            return {
                "nomConjoint":     fam.nomConjoint     or "",
                "prenomConjoint":  fam.prenomConjoint  or "",
                "adresseConjoint": fam.adresseConjoint or "",
                "telConjoint":     fam.telConjoint     or "",
                "emailConjoint":   fam.emailConjoint   or "",
                "acteMariage":     clean_file_url(fam.acteMariage),
            }
        return {}

    # ── Banque ─────────────────────────────────────────────
    def get_rib(self, obj):
        b = self._get_related_data(obj)['banque']
        return b.rib if b else ""

    def get_banque(self, obj):
        b = self._get_related_data(obj)['banque']
        return b.banque.nom if b and b.banque else ""

    def get_agence(self, obj):
        b = self._get_related_data(obj)['banque']
        return b.agence.nom if b and b.agence else ""

    def get_villeAgence(self, obj):
        b = self._get_related_data(obj)['banque']
        return b.agence.ville if b and b.agence else ""

    def get_photoRib(self, obj):
        b = self._get_related_data(obj)['banque']
        return clean_file_url(b.photoRib) if b else None

    # ── CIN ────────────────────────────────────────────────
    def get_cin(self, obj):
        c = self._get_related_data(obj)['cin']
        if c:
            return {
                "numero":          c.numeroCin or "",
                "dateDelivrance":  str(c.dateCin) if c.dateCin else "",
                "lieuDelivrance":  c.lieuCin or "",
                "numeroDuplicata": getattr(c, 'numeroDuplicata', ""),
                "dateDuplicata":   str(c.dateDuplicata) if getattr(c, 'dateDuplicata', None) else "",
                "lieuDuplicata":   getattr(c, 'lieuDuplicata', ""),
            }
        return None

    def get_dateDelivranceCin(self, obj):
        c = self._get_related_data(obj)['cin']
        return str(c.dateCin) if c and c.dateCin else ""

    def get_lieuDelivranceCin(self, obj):
        c = self._get_related_data(obj)['cin']
        return c.lieuCin if c else ""

    # ── Contrat ────────────────────────────────────────────
    def get_contrat(self, obj):
        c = Contrat.objects.filter(personnelle=obj).last()
        if c:
            return {
                "numero":       getattr(c, 'NumeroContrat', ""),
                "type":         c.typeContrat.TypeContrat if getattr(c, 'typeContrat', None) else None,
                "salaire":      getattr(c, 'salaire', 0),
                "periodeEssai": getattr(c, 'periodeEssai', ""),
                "dateFinEssai": str(c.dateFinEssai) if getattr(c, 'dateFinEssai', None) else "",
                "photo":        clean_file_url(c.photoContrat) if getattr(c, 'photoContrat', None) else None,
            }
        return None