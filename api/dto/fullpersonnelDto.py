from rest_framework import serializers
from api.models import *

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
    class Meta:
        model = Enfant
        fields = '__all__'

class ContactUrgenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUrgences
        fields = ['id', 'nom', 'telephone', 'adresse', 'relation']
        depth = 1

class DiplomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diplome
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
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
class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'

# ==========================================
# 3. SERIALIZER DE LECTURE (GET FULL)
# ==========================================

class PersonnelFullSerializer(serializers.ModelSerializer):
    # --- Alias pour le Front-end ---
    emailPersonnel = serializers.CharField(source='emailPerso', default="")
    telephonePersonnel = serializers.CharField(source='telPerso', default="")
    
    # --- Relations imbriquées ---
    enfants = EnfantSerializer(many=True, read_only=True, source='Enfant')
    contactsUrgence = ContactUrgenceSerializer(many=True, read_only=True, source='contactUrgence')
    diplomes = DiplomeSerializer(many=True, read_only=True, source='Diplome')
    experiences = ExperienceSerializer(many=True, read_only=True, source='Experience')
    formations = FormationSerializer(many=True, read_only=True, source='Formation')

    # --- Champs calculés ---
    cin = serializers.SerializerMethodField()
    dateDelivranceCin = serializers.SerializerMethodField()
    lieuDelivranceCin = serializers.SerializerMethodField()
    
    nif = serializers.ReadOnlyField(source='propos_list.first.nif', default="")
    stat = serializers.ReadOnlyField(source='propos_list.first.stat', default="")
    cnaps = serializers.ReadOnlyField(source='propos_list.first.numeroCnaps', default="")
    emailProfessionnel = serializers.ReadOnlyField(source='propos_list.first.email', default="")
    contactProfessionnel = serializers.ReadOnlyField(source='propos_list.first.tel', default="")
    etatCivil = serializers.ReadOnlyField(source='propos_list.first.etatCivil.id', default=None)
    nombreEnfants = serializers.ReadOnlyField(source='propos_list.first.nombreEnfant', default=0)
    
    nomPere = serializers.SerializerMethodField()
    prenomPere = serializers.SerializerMethodField()
    nomMere = serializers.SerializerMethodField()
    prenomMere = serializers.SerializerMethodField()
    
    rib = serializers.SerializerMethodField()
    banque = serializers.SerializerMethodField() # Utilise la méthode get_banque
    agence = serializers.SerializerMethodField()
    
    conjoint = serializers.SerializerMethodField()
    photoUrl = serializers.SerializerMethodField()
    contrat = serializers.SerializerMethodField()
    poste_superieur = serializers.SerializerMethodField()
    service_actuel = serializers.SerializerMethodField()
    financement_actuel = serializers.SerializerMethodField()
    date_embauche = serializers.SerializerMethodField()

    class Meta:
        model = Personnelles
        # CRUCIAL : On définit l'ordre d'affichage ici
        fields = [
            'id', 'nom', 'prenom', 'sexe', 'dateNaissance', 'lieuNaissance', 'adresse',
            'emailPersonnel', 'telephonePersonnel', 'photoUrl',
            'cin','date_embauche', 'poste_superieur', 'service_actuel', 'financement_actuel',
            'contrat', 'dateDelivranceCin', 'lieuDelivranceCin',
            'etatCivil', 'nombreEnfants', 'conjoint',
            'nomPere', 'prenomPere', 'nomMere', 'prenomMere',
            'emailProfessionnel', 'contactProfessionnel', 'nif', 'stat', 'cnaps',
            'rib', 'banque', 'agence',
            'enfants', 'contactsUrgence', 'diplomes', 'experiences', 'formations',
            'photoResidence', 'cinphoto', 'acteNaissance', 'casierjudiciaire'
        ]

    class Meta:
        model = Personnelles
        fields = '__all__'
    

    def _get_famille(self, obj):
        return Famille.objects.filter(personnelle=obj).first()

    def _get_propos(self, obj):
        return obj.propos_list.first()

    def get_cin(self, obj):
        c = obj.cins.first()
        return c.numeroCin if c else ""

    def get_dateDelivranceCin(self, obj):
        c = obj.cins.first()
        return str(c.dateCin) if c else ""

    def get_lieuDelivranceCin(self, obj):
        c = obj.cins.first()
        return c.lieuCin if c else ""

    def get_etatCivil(self, obj):
        p = self._get_propos(obj)
        return p.etatCivil.id if p and p.etatCivil else ""

    def get_nombreEnfants(self, obj):
        p = self._get_propos(obj)
        return p.nombreEnfant if p else 0

    def get_emailProfessionnel(self, obj):
        p = self._get_propos(obj)
        return p.email if p else ""

    def get_nif(self, obj):
        p = self._get_propos(obj)
        return p.nif if p else ""

    def get_stat(self, obj):
        p = self._get_propos(obj)
        return p.stat if p else ""

    def get_cnaps(self, obj):
        p = self._get_propos(obj)
        return p.numeroCnaps if p else ""

    def get_contactProfessionnel(self, obj):
        p = self._get_propos(obj)
        return p.tel if p else ""

    def get_nomPere(self, obj):
        f = self._get_famille(obj)
        return f.nomPere if f else ""

    def get_prenomPere(self, obj):
        f = self._get_famille(obj)
        return f.prenomPere if f else ""

    def get_nomMere(self, obj):
        f = self._get_famille(obj)
        return f.nomMere if f else ""

    def get_prenomMere(self, obj):
        f = self._get_famille(obj)
        return f.prenomMere if f else ""

    def get_rib(self, obj):
        # On importe ici pour éviter les imports circulaires
        from api.models import CoordonneesBancaires 
        # On cherche directement dans la table en filtrant par l'ID du personnel
        b = CoordonneesBancaires.objects.filter(personnelle=obj).first()
        return b.rib if b else ""

    def get_banque(self, obj):
        from api.models import CoordonneesBancaires
        b = CoordonneesBancaires.objects.filter(personnelle=obj).first()
        return b.banque.nom if b and b.banque else ""

    def get_agence(self, obj):
        from api.models import CoordonneesBancaires
        b = CoordonneesBancaires.objects.filter(personnelle=obj).first()
        return b.agence.nom if b and b.agence else ""
    def get_conjoint(self, obj):
        f = self._get_famille(obj)
        if f:
            return {
                "nomConjoint": f.nomConjoint or "",
                "prenomConjoint": f.prenomConjoint or "",
                "adresseConjoint": f.adresseConjoint or "",
                "telConjoint": f.telConjoint or "",
                "emailConjoint": f.emailConjoint or ""
            }
        return {}

    def get_photoUrl(self, obj):
        p = obj.photos.first()
        return p.data.url if p and p.data else None
    def get_contrat(self, obj):
        # On cherche directement dans la table Contrat le premier lié à ce personnel
        c = Contrat.objects.filter(personnelle=obj).first()
        if c:
            return {
                "numero": getattr(c, 'NumeroContrat', ""),
                "type": c.typeContrat.TypeContrat if getattr(c, 'typeContrat', None) else None,
                "periodeEssai": getattr(c, 'periodeEssai', ""),
                "dateFinEssai": str(c.dateFinEssai) if getattr(c, 'dateFinEssai', None) else "",
                "photo": c.photoContrat.url if (getattr(c, 'photoContrat', None) and c.photoContrat) else None
            }
        return None

    # --- LOGIQUE POUR LA FONCTION (Poste, Service, Financement) ---
    def _get_fonction_info(self, obj):
        if not hasattr(self, '_cached_fonction'):
            # On essaie 'personnelle', si ça échoue, on peut tester 'personnel'
            f = Fonctions.objects.filter(personnelle=obj).first()
            if not f:
                # Tentative de secours au cas où le nom du champ est différent
                # f = Fonction.objects.filter(personnel=obj).first() 
                pass
            self._cached_fonction = f
        return self._cached_fonction

    def get_poste_superieur(self, obj):
        f = self._get_fonction_info(obj)
        return f.poste.nom if f and f.poste else "Non défini"

    def get_service_actuel(self, obj):
        f = self._get_fonction_info(obj)
        return f.service.nom if f and f.service else "Non défini"

    def get_financement_actuel(self, obj):
        f = self._get_fonction_info(obj)
        return f.financement.nom if f and f.financement else None

    def get_date_embauche(self, obj):
        f = self._get_fonction_info(obj)
        return f.dateDebut if f else None

# ==========================================
# 4. SERIALIZER DE MISE À JOUR (UPDATE)
# ==========================================

class PersonnelUpdateSerializer(serializers.ModelSerializer):
    # Champs pour correspondre au format du front
    emailPersonnel = serializers.EmailField(source='emailPerso', required=False)
    telephonePersonnel = serializers.CharField(source='telPerso', required=False)
    
    # Champs virtuels pour les tables liées
    cin = serializers.CharField(required=False, allow_blank=True)
    dateDelivranceCin = serializers.DateField(required=False, allow_null=True)
    lieuDelivranceCin = serializers.CharField(required=False, allow_blank=True)
    
    nif = serializers.CharField(required=False, allow_blank=True)
    stat = serializers.CharField(required=False, allow_blank=True)
    cnaps = serializers.CharField(required=False, allow_blank=True)
    emailProfessionnel = serializers.EmailField(required=False, allow_blank=True)
    contactProfessionnel = serializers.CharField(required=False, allow_blank=True)
    etatCivil = serializers.IntegerField(required=False)
    nombreEnfants = serializers.IntegerField(required=False)

    nomPere = serializers.CharField(required=False, allow_blank=True)
    nomMere = serializers.CharField(required=False, allow_blank=True)

    
    nomConjoint = serializers.CharField(required=False, allow_blank=True)
    prenomConjoint = serializers.CharField(required=False, allow_blank=True)
    telConjoint = serializers.CharField(required=False, allow_blank=True)
    emailConjoint = serializers.CharField(required=False, allow_blank=True)
    adresseConjoint = serializers.CharField(required=False, allow_blank=True)

    rib = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Personnelles
        fields = [
            'nom', 'prenom', 'dateNaissance', 'lieuNaissance', 'adresse', 
            'emailPersonnel', 'telephonePersonnel', 'sexe',
            'cin', 'dateDelivranceCin', 'lieuDelivranceCin',
            'nif', 'stat', 'cnaps', 'emailProfessionnel', 'contactProfessionnel', 'etatCivil', 'nombreEnfants',
            'nomPere', 'prenomPere', 'nomMere', 'prenomMere',
            'nomConjoint', 'prenomConjoint', 'telConjoint', 'emailConjoint', 'adresseConjoint',
            'rib'
        ]

    def update(self, instance, validated_data):
        # Séparation des données liées
        cin_data = {
            'numeroCin': validated_data.pop('cin', None),
            'dateCin': validated_data.pop('dateDelivranceCin', None),
            'lieuCin': validated_data.pop('lieuDelivranceCin', None),
        }
        
        propos_data = {
            'nif': validated_data.pop('nif', None),
            'stat': validated_data.pop('stat', None),
            'numeroCnaps': validated_data.pop('cnaps', None),
            'email': validated_data.pop('emailProfessionnel', None),
            'tel': validated_data.pop('contactProfessionnel', None),
            'etatCivil_id': validated_data.pop('etatCivil', None),
            'nombreEnfant': validated_data.pop('nombreEnfants', None),
        }
        
        famille_data = {
            'nomPere': validated_data.pop('nomPere', None),
            'prenomPere': validated_data.pop('prenomPere', None),
            'nomMere': validated_data.pop('nomMere', None),
            'prenomMere': validated_data.pop('prenomMere', None),
            'nomConjoint': validated_data.pop('nomConjoint', None),
            'prenomConjoint': validated_data.pop('prenomConjoint', None),
            'telConjoint': validated_data.pop('telConjoint', None),
            'emailConjoint': validated_data.pop('emailConjoint', None),
            'adresseConjoint': validated_data.pop('adresseConjoint', None),
        }

        rib_val = validated_data.pop('rib', None)

        # 1. Update Personnel
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 2. Update CIN
        if any(v is not None for v in cin_data.values()):
            c_obj, _ = Cins.objects.get_or_create(personnelle=instance)
            for k, v in cin_data.items():
                if v is not None: setattr(c_obj, k, v)
            c_obj.save()

        # 3. Update Propos
        if any(v is not None for v in propos_data.values()):
            p_obj, _ = Propos.objects.get_or_create(personnelle=instance)
            for k, v in propos_data.items():
                if v is not None: setattr(p_obj, k, v)
            p_obj.save()

        # 4. Update Famille
        if any(v is not None for v in famille_data.values()):
            f_obj, _ = Famille.objects.get_or_create(personnelle=instance)
            for k, v in famille_data.items():
                if v is not None: setattr(f_obj, k, v)
            f_obj.save()

        # 5. Update RIB
        if rib_val is not None:
            from api.models import CoordonneesBancaires
            # On cherche l'enregistrement existant ou on en crée un nouveau
            r_obj, created = CoordonneesBancaires.objects.get_or_create(personnelle=instance)
            r_obj.rib = rib_val
            r_obj.save()

        return instance