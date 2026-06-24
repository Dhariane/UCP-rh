from urllib.parse import urlparse, unquote

from rest_framework import serializers
from api.models import *
from api.models.propos.personnelles import Personnelles


# ==========================================
# HELPER GLOBAL
# ==========================================

def clean_file_url(file_field):
    """Convertit n'importe quel FileField en URL propre /media/xxx"""
    if not file_field:
        return None
    try:
        name = file_field.name
        if not name:
            return None
        if 'http' in name or '%' in name:
            decoded = unquote(name)
            parsed = urlparse(decoded)
            return f"http://127.0.0.1:8000{parsed.path}"
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
# SERIALIZERS CONGE + SOLDE CONGE
# ==========================================

class CongeSerializer(serializers.ModelSerializer):
    type_conge   = serializers.SerializerMethodField()
    statut       = serializers.SerializerMethodField()
    validated_by = serializers.SerializerMethodField()

    def get_type_conge(self, obj):
        return {
            "id": obj.type_conge.id,
            "nom": getattr(obj.type_conge, 'nom', str(obj.type_conge))
        }

    def get_statut(self, obj):
        return {
            "id": obj.statut.id,
            "nom": getattr(obj.statut, 'nom', str(obj.statut))
        }

    def get_validated_by(self, obj):
        if obj.validated_by:
            login = obj.validated_by
            personnelle = login.personnelle
            return {
                "id": login.id,
                "email": str(login.email),  # ton Login a email comme FK vers Propos
                "full_name": f"{personnelle.prenom} {personnelle.nom}".strip() if personnelle else str(login)
            }
        return None

    class Meta:
        model = Conge
        fields = [
            'id', 'type_conge', 'solde_conge', 'date_debut', 'date_fin',
            'nombre_jours', 'description', 'statut', 'validated_by','etape_validation',
            'created_at', 'updated_at'
        ]


class SoldeCongeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldeConge
        fields = ['id', 'annee', 'total', 'utilise', 'reste']


# ==========================================
# SERIALIZER PRINCIPAL
# ==========================================

class PersonnelFullSerializer(serializers.ModelSerializer):
    # --- Relations directes ---
    emailPersonnel     = serializers.CharField(source='emailPerso', default="")
    telephonePersonnel = serializers.CharField(source='telPerso', default="")
    contactsUrgence    = ContactUrgenceSerializer(many=True, read_only=True, source='contactUrgence')
    diplomes           = DiplomeSerializer(many=True, read_only=True)
    experiences        = ExperienceSerializer(many=True, read_only=True, source='Experience')
    formations         = FormationSerializer(many=True, read_only=True, source='Formation')
    enfants            = EnfantSerializer(many=True, read_only=True, source='Enfant')
    conges             = CongeSerializer(many=True, read_only=True)

    # --- Champs calculés ---
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
    soldes_conge         = serializers.SerializerMethodField()
    photoResidence       = serializers.SerializerMethodField()
    cinphoto             = serializers.SerializerMethodField()
    acteNaissance        = serializers.SerializerMethodField()
    casierjudiciaire     = serializers.SerializerMethodField()

    class Meta:
        model = Personnelles
        fields = [
            'id','matricule', 'nom', 'prenom', 'sexe', 'dateNaissance', 'lieuNaissance', 'adresse',
            'emailPersonnel', 'telephonePersonnel', 'photoUrl', 'quartier', 'ville',
            'cin', 'date_embauche', 'fonction', 'date_sortie', 'poste_superieur',
            'service_actuel', 'financement_actuel',
            'contrat', 'dateDelivranceCin', 'lieuDelivranceCin',
            'etatCivil', 'nombreEnfants', 'conjoint',
            'nomPere', 'nomMere',
            'emailProfessionnel', 'contactProfessionnel', 'nif', 'stat', 'cnaps',
            'rib', 'banque', 'agence', 'villeAgence', 'photoRib',
            'enfants', 'contactsUrgence', 'diplomes', 'experiences', 'formations',
            'conges', 'soldes_conge',
            'photoResidence', 'cinphoto', 'acteNaissance', 'casierjudiciaire','is_active'
        ]

    # ══════════════════════════════════════════════════════
    # CACHE — utilise les prefetch_related du controller
    # ══════════════════════════════════════════════════════

    def _get_contrat(self, obj):
        """
        Utilise le prefetch 'contrats' fait dans le controller.
        NE fait PAS de nouvelle requête SQL.
        """
        if not hasattr(obj, '_contrat_cache'):
            # obj.contrats est déjà prefetché → .all() ne touche pas la DB
            contrats = list(obj.contrats.all())
            # On prend le plus récent (trié par -dateDebut dans le Prefetch du controller)
            obj._contrat_cache = contrats[0] if contrats else None
        return obj._contrat_cache

    def _get_propos(self, obj):
        """Requête légère sur Propos (non prefetché, mais table petite)."""
        if not hasattr(obj, '_propos_cache'):
            obj._propos_cache = Propos.objects.filter(personnelle=obj).select_related('etatCivil').last()
        return obj._propos_cache

    def _get_famille(self, obj):
        if not hasattr(obj, '_famille_cache'):
            obj._famille_cache = Famille.objects.filter(personnelle=obj).first()
        return obj._famille_cache

    def _get_banque(self, obj):
        if not hasattr(obj, '_banque_cache'):
            obj._banque_cache = CoordonneesBancaires.objects.filter(personnelle=obj).select_related('banque', 'agence').first()
        return obj._banque_cache

    def _get_cin(self, obj):
        """Utilise le prefetch 'cins' fait dans le controller."""
        if not hasattr(obj, '_cin_cache'):
            cins = list(obj.cins.all())
            obj._cin_cache = cins[0] if cins else None
        return obj._cin_cache

    # ══════════════════════════════════════════════════════
    # FICHIERS DIRECTS SUR Personnelles
    # ══════════════════════════════════════════════════════

    def get_photoResidence(self, obj):
        return clean_file_url(obj.photoResidence)

    def get_cinphoto(self, obj):
        return clean_file_url(obj.cinphoto)

    def get_acteNaissance(self, obj):
        return clean_file_url(obj.acteNaissance)

    def get_casierjudiciaire(self, obj):
        return clean_file_url(obj.casierjudiciaire)

    # ══════════════════════════════════════════════════════
    # PHOTO PROFIL
    # ══════════════════════════════════════════════════════

    def get_photoUrl(self, obj):
        # Utilise le prefetch 'photos' du controller
        photos = list(obj.photos.all())
        if photos and photos[0].data:
            try:
                return photos[0].data.url
            except Exception:
                return None
        return None

    # ══════════════════════════════════════════════════════
    # CONTRAT (via prefetch — zéro requête SQL supplémentaire)
    # ══════════════════════════════════════════════════════

    def get_fonction(self, obj):
        c = self._get_contrat(obj)
        return c.fonction.nom if c and c.fonction else ""

    def get_date_embauche(self, obj):
        c = self._get_contrat(obj)
        return str(c.dateDebut) if c and c.dateDebut else None

    def get_date_sortie(self, obj):
        c = self._get_contrat(obj)
        return str(c.dateFin) if c and c.dateFin else None

    def get_financement_actuel(self, obj):
        c = self._get_contrat(obj)
        return c.financement.nom if c and c.financement else "Non défini"

    def get_service_actuel(self, obj):
        c = self._get_contrat(obj)
        return c.service.nom if c and c.service else "Non défini"

    def get_poste_superieur(self, obj):
        """
        Cherche le chef du même service.
        On fait UNE seule requête SQL ciblée (pas de Fonctions.personnelle_id).
        """
        c = self._get_contrat(obj)
        if not c or not c.service:
            return "Non défini"

        from api.models.fonction.contrat import Contrat as ContratModel
        contrat_chef = (
            ContratModel.objects
            .filter(
                service=c.service,
                fonction__is_chef=True,
                dateFin__isnull=True,
            )
            .exclude(personnelle=obj)
            .select_related('fonction')
            .first()
        )
        return contrat_chef.fonction.nom if contrat_chef else "Non défini"

    def get_contrat(self, obj):
        c = self._get_contrat(obj)
        if c:
            return {
                "numero":       getattr(c, 'NumeroContrat', ""),
                "type":         c.typeContrat.TypeContrat if getattr(c, 'typeContrat', None) else None,
                "salaire":      str(getattr(c, 'salaire', 0) or 0),
                "periodeEssai": getattr(c, 'periodeEssai', ""),
                "dateFinEssai": str(c.dateFinEssai) if getattr(c, 'dateFinEssai', None) else "",
                "photo":        clean_file_url(c.photoContrat) if getattr(c, 'photoContrat', None) else None,
                "fonction":     c.fonction.nom if c.fonction else "",
                "service":      c.service.nom if c.service else "",
                "financement":  c.financement.nom if c.financement else "",
                "dateDebut":    str(c.dateDebut) if c.dateDebut else "",
                "dateFin":      str(c.dateFin) if c.dateFin else "",
            }
        return None

    # ══════════════════════════════════════════════════════
    # SOLDES CONGÉ
    # ══════════════════════════════════════════════════════

    def get_soldes_conge(self, obj):
        soldes = SoldeConge.objects.filter(personnel=obj).order_by('-annee')
        return SoldeCongeSerializer(soldes, many=True).data

    # ══════════════════════════════════════════════════════
    # PROPOS
    # ══════════════════════════════════════════════════════

    def get_nif(self, obj):
        p = self._get_propos(obj)
        return p.nif if p else ""

    def get_stat(self, obj):
        p = self._get_propos(obj)
        return p.stat if p else ""

    def get_cnaps(self, obj):
        p = self._get_propos(obj)
        return p.numeroCnaps if p else ""

    def get_emailProfessionnel(self, obj):
        p = self._get_propos(obj)
        return p.email if p else ""

    def get_contactProfessionnel(self, obj):
        p = self._get_propos(obj)
        return p.tel if p else ""

    def get_etatCivil(self, obj):
        p = self._get_propos(obj)
        return p.etatCivil.id if p and p.etatCivil else None

    def get_nombreEnfants(self, obj):
        p = self._get_propos(obj)
        return p.nombreEnfant if p else 0

    # ══════════════════════════════════════════════════════
    # FAMILLE
    # ══════════════════════════════════════════════════════

    def get_nomPere(self, obj):
        fam = self._get_famille(obj)
        return fam.nomPere if fam else ""

    def get_nomMere(self, obj):
        fam = self._get_famille(obj)
        return fam.nomMere if fam else ""

    def get_conjoint(self, obj):
        fam = self._get_famille(obj)
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

    # ══════════════════════════════════════════════════════
    # BANQUE
    # ══════════════════════════════════════════════════════

    def get_rib(self, obj):
        b = self._get_banque(obj)
        return b.rib if b else ""

    def get_banque(self, obj):
        b = self._get_banque(obj)
        return b.banque.nom if b and b.banque else ""

    def get_agence(self, obj):
        b = self._get_banque(obj)
        return b.agence.nom if b and b.agence else ""

    def get_villeAgence(self, obj):
        b = self._get_banque(obj)
        return b.agence.ville if b and b.agence else ""

    def get_photoRib(self, obj):
        b = self._get_banque(obj)
        return clean_file_url(b.photoRib) if b else None

    # ══════════════════════════════════════════════════════
    # CIN (via prefetch 'cins' du controller)
    # ══════════════════════════════════════════════════════

    def get_cin(self, obj):
        c = self._get_cin(obj)
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
        c = self._get_cin(obj)
        return str(c.dateCin) if c and c.dateCin else ""

    def get_lieuDelivranceCin(self, obj):
        c = self._get_cin(obj)
        return c.lieuCin if c else ""
