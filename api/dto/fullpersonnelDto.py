import json

from rest_framework import serializers
from api.models import *
from api.services.personnelles.diplome.experienceService import ExperienceService
from api.services.personnelles.fonction import ServiceService
from api.services.personnelles.fonction.fonctionService import FonctionService
from api.services.personnelles.propos.enfantService import EnfantService

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
    quartier = serializers.CharField(default="")
    ville = serializers.CharField(default="")
    
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
    nomMere = serializers.SerializerMethodField()
    
    rib = serializers.SerializerMethodField()
    banque = serializers.SerializerMethodField() 
    agence = serializers.SerializerMethodField()
    photoRib = serializers.SerializerMethodField()
    
    conjoint = serializers.SerializerMethodField()
    photoUrl = serializers.SerializerMethodField()
    contrat = serializers.SerializerMethodField()
    poste_superieur = serializers.SerializerMethodField()
    service_actuel = serializers.SerializerMethodField()
    financement_actuel = serializers.SerializerMethodField()
    date_embauche = serializers.SerializerMethodField()
    fonction = serializers.SerializerMethodField()
    date_sortie = serializers.SerializerMethodField()

    class Meta:
        model = Personnelles
        fields = [
            'id', 'nom', 'prenom', 'sexe', 'dateNaissance', 'lieuNaissance', 'adresse',
            'emailPersonnel', 'telephonePersonnel', 'photoUrl','quartier', 'ville',
            'cin','date_embauche','fonction','date_sortie', 'poste_superieur', 'service_actuel', 'financement_actuel',
            'contrat', 'dateDelivranceCin', 'lieuDelivranceCin',
            'etatCivil', 'nombreEnfants', 'conjoint',
            'nomPere','nomMere',
            'emailProfessionnel', 'contactProfessionnel', 'nif', 'stat', 'cnaps',
            'rib', 'banque', 'agence','photoRib',
            'enfants', 'contactsUrgence', 'diplomes', 'experiences', 'formations',
            'photoResidence', 'cinphoto', 'acteNaissance', 'casierjudiciaire'
        ]
    def _get_fonction_info(self, obj):
        if not hasattr(self, '_cached_fonction'):
            # On récupère la ligne de la table Fonctions liée à ce personnel
            self._cached_fonction = Fonctions.objects.filter(personnelle=obj).first()
        return self._cached_fonction
    def _get_famille(self, obj):
        return Famille.objects.filter(personnelle=obj).first()
    def get_fonction(self, obj):
        f = self._get_fonction_info(obj)
        return f.nom if f else "Non défini"
    def get_date_sortie(self, obj):
        f = self._get_fonction_info(obj)
        return str(f.dateFin) if f and f.dateFin else None
    def _get_propos(self, obj):
        return obj.propos_list.first()

    def get_cin(self, obj):
        c = obj.cins.first()
        if c:
            return {
                "numero": c.numeroCin or "",
                "dateDelivrance": str(c.dateCin) if c.dateCin else "",
                "lieuDelivrance": c.lieuCin or "",
                "dateDuplicata": str(c.dateDuplicata) if getattr(c, 'dateDuplicata', None) else "",
                "lieuDuplicata": c.lieuDuplicata if getattr(c, 'lieuDuplicata', None) else "",
                "numeroDuplicata": getattr(c, 'numeroDuplicata', ""), # <--- ÉTAIT MANQUANT
                "dateDuplicata": str(c.dateDuplicata) if getattr(c, 'dateDuplicata', None) else "",
                "lieuDuplicata": getattr(c, 'lieuDuplicata', "")
            }
        return None
    def get_photoRib(self, obj):
        from api.models import CoordonneesBancaires
        b = CoordonneesBancaires.objects.filter(personnelle=obj).first()
        return b.photoRib.url if b and b.photoRib else None

    def get_dateDelivranceCin(self, obj):
        c = obj.cins.first()
        return str(c.dateCin) if c else ""

    def get_lieuDelivranceCin(self, obj):
        c = obj.cins.first()
        return c.lieuCin if c else ""

    def get_nomPere(self, obj):
        f = self._get_famille(obj)
        return f.nomPere if f else ""

    def get_nomMere(self, obj):
        f = self._get_famille(obj)
        return f.nomMere if f else ""

    def get_rib(self, obj):
        from api.models import CoordonneesBancaires 
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
                "emailConjoint": f.emailConjoint or "",
                "acteMariage": f.acteMariage.url if f.acteMariage else None
            }
        return {}

    def get_photoUrl(self, obj):
        p = obj.photos.first()
        return p.data.url if p and p.data else None

    def get_contrat(self, obj):
        # On récupère le dernier contrat en date
        c = Contrat.objects.filter(personnelle=obj).last() 
        if c:
            return {
                "numero": getattr(c, 'NumeroContrat', ""),
                "type": c.typeContrat.TypeContrat if getattr(c, 'typeContrat', None) else None,
                "salaire": getattr(c, 'salaire', 0), # Ajout du salaire ici
                "periodeEssai": getattr(c, 'periodeEssai', ""),
                "dateFinEssai": str(c.dateFinEssai) if getattr(c, 'dateFinEssai', None) else "",
                "photo": c.photoContrat.url if (getattr(c, 'photoContrat', None) and c.photoContrat) else None
            }
        return None

    def _get_fonction_info(self, obj):
        if not hasattr(self, '_cached_fonction'):
            f = Fonctions.objects.filter(personnelle=obj).first()
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

# from rest_framework import serializers
# from api.models import Personnelles, Cins, Propos, Familles, CoordonneesBancaires, Enfant, Experience, Diplome, Formation, ContactUrgence, Contrat


class PersonnelUpdateSerializer(serializers.ModelSerializer):
    # --- CONFIGURATION DES CHAMPS (Aliasing pour le Frontend) ---
    emailPersonnel = serializers.EmailField(source='emailPerso', required=False)
    telephonePersonnel = serializers.CharField(source='telPerso', required=False)
    num_cin_input = serializers.CharField(required=False, allow_blank=True)
    dateDelivranceCin = serializers.DateField(required=False, allow_null=True)
    lieuDelivranceCin = serializers.CharField(required=False, allow_blank=True)
    
    # --- CHAMPS PROPOS & FAMILLE ---
    nif = serializers.CharField(required=False, allow_blank=True)
    stat = serializers.CharField(required=False, allow_blank=True)
    cnaps = serializers.CharField(required=False, allow_blank=True)
    emailProfessionnel = serializers.EmailField(required=False, allow_blank=True)
    contactProfessionnel = serializers.CharField(required=False, allow_blank=True)
    etatCivil = serializers.IntegerField(required=False)
    nombreEnfants = serializers.IntegerField(required=False)
    
    # --- AJOUT DU CHAMP VILLE AGENCE ---
    villeAgence = serializers.CharField(required=False, allow_blank=True)
    
    # --- LISTES D'ACTIONS (EXPERIENCES, DIPLOMES, FORMATIONS) ---
    ajouter_experiences = serializers.ListField(required=False)
    mettre_a_jour_experiences = serializers.ListField(required=False)
    supprimer_experiences = serializers.ListField(required=False)

    ajouter_diplomes = serializers.ListField(required=False)
    mettre_a_jour_diplomes = serializers.ListField(required=False)
    supprimer_diplomes = serializers.ListField(required=False)

    ajouter_formations = serializers.ListField(required=False)
    mettre_a_jour_formations = serializers.ListField(required=False)
    supprimer_formations = serializers.ListField(required=False)

    # --- LISTES D'ACTIONS (ENFANTS & CONTACTS) ---
    ajouter_enfants = serializers.ListField(required=False)
    mettre_a_jour_enfants = serializers.ListField(required=False)
    supprimer_enfants = serializers.ListField(required=False)

    ajouter_contacts_urgence = serializers.ListField(required=False)
    mettre_a_jour_contacts_urgence = serializers.ListField(required=False)
    supprimer_contacts_urgence = serializers.ListField(required=False)

    class Meta:
        model = Personnelles
        fields = '__all__'

    def _parse_json(self, data):
        """Utilitaire pour décoder le JSON venant de Postman ou React"""
        if not data: return []
        try:
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], str):
                return json.loads(data[0])
            if isinstance(data, str):
                return json.loads(data)
            return data
        except: return []

    def update(self, instance, validated_data):
        # 1. EXTRACTION DES LISTES
        add_exp = self._parse_json(validated_data.pop('ajouter_experiences', []))
        upd_exp = self._parse_json(validated_data.pop('mettre_a_jour_experiences', []))
        del_exp = self._parse_json(validated_data.pop('supprimer_experiences', []))

        add_dip = self._parse_json(validated_data.pop('ajouter_diplomes', []))
        upd_dip = self._parse_json(validated_data.pop('mettre_a_jour_diplomes', []))
        del_dip = self._parse_json(validated_data.pop('supprimer_diplomes', []))

        add_form = self._parse_json(validated_data.pop('ajouter_formations', []))
        upd_form = self._parse_json(validated_data.pop('mettre_a_jour_formations', []))
        del_form = self._parse_json(validated_data.pop('supprimer_formations', []))

        add_enf = self._parse_json(validated_data.pop('ajouter_enfants', []))
        upd_enf = self._parse_json(validated_data.pop('mettre_a_jour_enfants', []))
        del_enf = self._parse_json(validated_data.pop('supprimer_enfants', []))

        add_con = self._parse_json(validated_data.pop('ajouter_contacts_urgence', []))
        upd_con = self._parse_json(validated_data.pop('mettre_a_jour_contacts_urgence', []))
        del_con = self._parse_json(validated_data.pop('supprimer_contacts_urgence', []))

        # 2. MISE À JOUR DE L'INSTANCE PERSONNELLE (CHAMPS DE BASE + VILLE AGENCE)
        sexe_id = validated_data.pop('sexe', None)
        if sexe_id:
            instance.sexe = sexe_id if isinstance(sexe_id, Sexes) else Sexes.objects.get(id=sexe_id)

        # On boucle sur le reste (adresse, ville, quartier, villeAgence, etc.)
        for attr, value in validated_data.items():
            if not isinstance(value, (list, dict)):
                setattr(instance, attr, value)
        instance.save()

        # 3. GESTION DES EXPÉRIENCES
        for item in add_exp:
            item.pop('id', None)
            Experience.objects.create(personnelle=instance, **item)
        for item in upd_exp:
            eid = item.pop('id', None)
            if eid: Experience.objects.filter(id=eid, personnelle=instance).update(**item)
        if del_exp: Experience.objects.filter(id__in=del_exp, personnelle=instance).delete()

        # 4. GESTION DES DIPLÔMES
        for item in add_dip:
            item.pop('id', None)
            if isinstance(item.get('photo'), str): item.pop('photo') 
            Diplome.objects.create(personnelle=instance, **item)
        for item in upd_dip:
            did = item.pop('id', None)
            if did:
                if isinstance(item.get('photo'), str): item.pop('photo')
                Diplome.objects.filter(id=did, personnelle=instance).update(**item)
        if del_dip: Diplome.objects.filter(id__in=del_dip, personnelle=instance).delete()

        # 5. GESTION DES FORMATIONS
        for item in add_form:
            item.pop('id', None)
            if isinstance(item.get('attestation'), str): item.pop('attestation')
            Formation.objects.create(personnelle=instance, **item)
        for item in upd_form:
            fid = item.pop('id', None)
            if fid:
                if isinstance(item.get('attestation'), str): item.pop('attestation')
                Formation.objects.filter(id=fid, personnelle=instance).update(**item)
        if del_form: Formation.objects.filter(id__in=del_form, personnelle=instance).delete()

        # 6. GESTION DES ENFANTS
        for item in add_enf:
            item.pop('id', None)
            s_id = item.pop('sexe', None)
            Enfant.objects.create(personnelle=instance, sexe_id=s_id, **item)
        for item in upd_enf:
            eid = item.pop('id', None)
            s_id = item.pop('sexe', None)
            if eid:
                if s_id: item['sexe_id'] = s_id
                Enfant.objects.filter(id=eid, personnelle=instance).update(**item)
        if del_enf: Enfant.objects.filter(id__in=del_enf, personnelle=instance).delete()

        # 7. GESTION DES CONTACTS D'URGENCE
        for item in add_con:
            item.pop('id', None)
            rel_id = item.pop('relation', None)
            ContactUrgences.objects.create(personnelle=instance, relation_id=rel_id, **item)
        for item in upd_con:
            cid = item.pop('id', None)
            rel_id = item.pop('relation', None)
            if cid:
                if rel_id: item['relation_id'] = rel_id
                ContactUrgences.objects.filter(id=cid, personnelle=instance).update(**item)
        if del_con: ContactUrgences.objects.filter(id__in=del_con, personnelle=instance).delete()

        # 8. MISE À JOUR DES TABLES LIÉES (CIN, PROPOS, FAMILLE, RIB)
        # --- CIN ---
        if any(k in validated_data for k in ['num_cin_input', 'dateDelivranceCin', 'lieuDelivranceCin']):
            cin_obj, _ = Cins.objects.get_or_create(personnelle=instance)
            if 'num_cin_input' in validated_data: cin_obj.numeroCin = validated_data.get('num_cin_input')
            if 'dateDelivranceCin' in validated_data: cin_obj.dateCin = validated_data.get('dateDelivranceCin')
            if 'lieuDelivranceCin' in validated_data: cin_obj.lieuCin = validated_data.get('lieuDelivranceCin')
            cin_obj.save()

        # --- PROPOS ---
        p_obj, _ = Propos.objects.get_or_create(personnelle=instance)
        if 'nif' in validated_data: p_obj.nif = validated_data.get('nif')
        if 'stat' in validated_data: p_obj.stat = validated_data.get('stat')
        if 'cnaps' in validated_data: p_obj.numeroCnaps = validated_data.get('cnaps')
        if 'emailProfessionnel' in validated_data: p_obj.email = validated_data.get('emailProfessionnel')
        if 'contactProfessionnel' in validated_data: p_obj.tel = validated_data.get('contactProfessionnel')
        if 'etatCivil' in validated_data: p_obj.etatCivil_id = validated_data.get('etatCivil')
        if 'nombreEnfants' in validated_data: p_obj.nombreEnfant = validated_data.get('nombreEnfants')
        p_obj.save()

        # --- FAMILLE ---
        f_obj, _ = Famille.objects.get_or_create(personnelle=instance)
        if 'nomPere' in validated_data: f_obj.nomPere = validated_data.get('nomPere')
        if 'nomMere' in validated_data: f_obj.nomMere = validated_data.get('nomMere')
        if 'nomConjoint' in validated_data: f_obj.nomConjoint = validated_data.get('nomConjoint')
        if 'prenomConjoint' in validated_data: f_obj.prenomConjoint = validated_data.get('prenomConjoint')
        if 'telConjoint' in validated_data: f_obj.telConjoint = validated_data.get('telConjoint')
        if 'emailConjoint' in validated_data: f_obj.emailConjoint = validated_data.get('emailConjoint')
        if 'adresseConjoint' in validated_data: f_obj.adresseConjoint = validated_data.get('adresseConjoint')
        f_obj.save()

        # --- RIB ---
        if 'rib' in validated_data:
            rib_obj, _ = CoordonneesBancaires.objects.get_or_create(personnelle=instance)
            rib_obj.rib = validated_data.get('rib')
            rib_obj.save()

        return instance