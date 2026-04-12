from decimal import Decimal
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
    # --- Alias et Relations ---
    emailPersonnel = serializers.CharField(source='emailPerso', default="")
    telephonePersonnel = serializers.CharField(source='telPerso', default="")
    enfants = EnfantSerializer(many=True, read_only=True, source='Enfant')
    contactsUrgence = ContactUrgenceSerializer(many=True, read_only=True, source='contactUrgence')
    diplomes = DiplomeSerializer(many=True, read_only=True, source='Diplome')
    experiences = ExperienceSerializer(many=True, read_only=True, source='Experience')
    formations = FormationSerializer(many=True, read_only=True, source='Formation')
    

    # --- Champs SerializerMethodField ---
    cin = serializers.SerializerMethodField()
    dateDelivranceCin = serializers.SerializerMethodField()
    lieuDelivranceCin = serializers.SerializerMethodField()
    nomPere = serializers.SerializerMethodField()
    nomMere = serializers.SerializerMethodField()
    rib = serializers.SerializerMethodField()
    banque = serializers.SerializerMethodField() 
    agence = serializers.SerializerMethodField()
    photoRib = serializers.SerializerMethodField()
    conjoint = serializers.SerializerMethodField()
    photoUrl = serializers.SerializerMethodField()
    contrat = serializers.SerializerMethodField()
    date_embauche = serializers.SerializerMethodField()
    date_sortie = serializers.SerializerMethodField()
    financement_actuel = serializers.SerializerMethodField()
    service_actuel = serializers.SerializerMethodField()
    poste_superieur = serializers.SerializerMethodField()
    fonction = serializers.SerializerMethodField()
    villeAgence = serializers.SerializerMethodField()

    # --- Champs ReadOnly (Propos) ---
    nif = serializers.SerializerMethodField()
    stat = serializers.SerializerMethodField()
    cnaps = serializers.SerializerMethodField()
    emailProfessionnel = serializers.SerializerMethodField()
    contactProfessionnel = serializers.SerializerMethodField()
    etatCivil = serializers.SerializerMethodField()
    nombreEnfants = serializers.SerializerMethodField()

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
            'rib', 'banque', 'agence','villeAgence','photoRib',
            'enfants', 'contactsUrgence', 'diplomes', 'experiences', 'formations',
            'photoResidence', 'cinphoto', 'acteNaissance', 'casierjudiciaire'
        ]

    # ==========================================================
    # LA MÉTHODE MANQUANTE (CACHE)
    # ==========================================================
    def _get_related_data(self, obj):
        """ Centralise la récupération avec un dictionnaire par ID d'objet """
        # On initialise le dictionnaire global s'il n'existe pas encore
        if not hasattr(self, '_cached_dict'):
            self._cached_dict = {}

        # Si les données de CET employé ne sont pas encore en cache, on les récupère
        if obj.id not in self._cached_dict:
            self._cached_dict[obj.id] = {
                'fonction': Fonctions.objects.filter(personnelle=obj).last(),
                'propos': Propos.objects.filter(personnelle=obj).last(), 
                'famille': Famille.objects.filter(personnelle=obj).first(),
                'banque': CoordonneesBancaires.objects.filter(personnelle=obj).first(),
                'cin': obj.cins.first()
            }
        
        return self._cached_dict[obj.id]
    
    def get_villeAgence(self, obj):
        b = self._get_related_data(obj)['banque']
        return b.agence.ville if b and b.agence else ""

    # Ensuite, tes getters appellent toujours la même chose :
    def get_fonction(self, obj):
        f = self._get_related_data(obj)['fonction']
        return f.nom if f else ""
    
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

    def get_financement_actuel(self, obj):
        f = self._get_related_data(obj)['fonction']
        return f.financement.nom if f and f.financement else "Non défini"

    def get_service_actuel(self, obj):
        f = self._get_related_data(obj)['fonction']
        return f.service.nom if f and f.service else "Non défini"

    def get_poste_superieur(self, obj):
        f = self._get_related_data(obj)['fonction']
        return f.poste.nom if f and f.poste else "Non défini"

    def get_date_embauche(self, obj):
        f = self._get_related_data(obj)['fonction']
        return str(f.dateDebut) if f and f.dateDebut else None

    def get_date_sortie(self, obj):
        f = self._get_related_data(obj)['fonction']
        return str(f.dateFin) if f and f.dateFin else None

    # --- Getters Famille ---
    def get_nomPere(self, obj):
        fam = self._get_related_data(obj)['famille']
        return fam.nomPere if fam else ""

    def get_nomMere(self, obj):
        fam = self._get_related_data(obj)['famille']
        return fam.nomMere if fam else ""

    # --- Getters Banque ---
    def get_rib(self, obj):
        b = self._get_related_data(obj)['banque']
        return b.rib if b else ""

    def get_banque(self, obj):
        b = self._get_related_data(obj)['banque']
        return b.banque.nom if b and b.banque else ""

    def get_agence(self, obj):
        b = self._get_related_data(obj)['banque']
        return b.agence.nom if b and b.agence else ""

    def get_photoRib(self, obj):
        b = self._get_related_data(obj)['banque']
        return b.photoRib.url if b and b.photoRib else None

    # --- Autres ---
    def get_cin(self, obj):
        c = self._get_related_data(obj)['cin']
        if c:
            return {
                "numero": c.numeroCin or "",
                "dateDelivrance": str(c.dateCin) if c.dateCin else "",
                "lieuDelivrance": c.lieuCin or "",
                "numeroDuplicata": getattr(c, 'numeroDuplicata', ""),
                "dateDuplicata": str(c.dateDuplicata) if getattr(c, 'dateDuplicata', None) else "",
                "lieuDuplicata": getattr(c, 'lieuDuplicata', "")
            }
        return None

    def get_dateDelivranceCin(self, obj):
        c = self._get_related_data(obj)['cin']
        return str(c.dateCin) if c else ""

    def get_lieuDelivranceCin(self, obj):
        c = self._get_related_data(obj)['cin']
        return c.lieuCin if c else ""

    def get_photoUrl(self, obj):
        p = obj.photos.first()
        return p.data.url if p and p.data else None

    def get_conjoint(self, obj):
        fam = self._get_related_data(obj)['famille']
        if fam:
            return {
                "nomConjoint": fam.nomConjoint or "",
                "prenomConjoint": fam.prenomConjoint or "",
                "adresseConjoint": fam.adresseConjoint or "",
                "telConjoint": fam.telConjoint or "",
                "emailConjoint": fam.emailConjoint or "",
                "acteMariage": fam.acteMariage.url if fam.acteMariage else None
            }
        return {}

    def get_contrat(self, obj):
        c = Contrat.objects.filter(personnelle=obj).last() 
        if c:
            return {
                "numero": getattr(c, 'NumeroContrat', ""),
                "type": c.typeContrat.TypeContrat if getattr(c, 'typeContrat', None) else None,
                "salaire": getattr(c, 'salaire', 0),
                "periodeEssai": getattr(c, 'periodeEssai', ""),
                "dateFinEssai": str(c.dateFinEssai) if getattr(c, 'dateFinEssai', None) else "",
                "photo": c.photoContrat.url if (getattr(c, 'photoContrat', None) and c.photoContrat) else None
            }
        return None
# ==========================================
# 4. SERIALIZER DE MISE À JOUR (UPDATE)
# ==========================================

# from rest_framework import serializers
# from api.models import Personnelles, Cins, Propos, Familles, CoordonneesBancaires, Enfant, Experience, Diplome, Formation, ContactUrgence, Contrat

import json


# class PersonnelUpdateSerializer(serializers.ModelSerializer):
#     # --- CONFIGURATION DES CHAMPS (Aliasing Frontend) ---
#     emailPersonnel = serializers.EmailField(source='emailPerso', required=False)
#     telephonePersonnel = serializers.CharField(source='telPerso', required=False)
#     num_cin_input = serializers.CharField(required=False, allow_blank=True)
#     dateDelivranceCin = serializers.DateField(required=False, allow_null=True)
#     lieuDelivranceCin = serializers.CharField(required=False, allow_blank=True)
#     dateDuplicataCin = serializers.DateField(required=False, allow_null=True)
#     lieuDuplicataCin = serializers.CharField(required=False, allow_blank=True)
#     photoCin = serializers.FileField(required=False, allow_null=True)
    
    
#     # --- CHAMPS PROPOS & FAMILLE ---
#     nif = serializers.CharField(required=False, allow_blank=True)
#     stat = serializers.CharField(required=False, allow_blank=True)
#     cnaps = serializers.CharField(required=False, allow_blank=True)
#     emailProfessionnel = serializers.EmailField(required=False, allow_blank=True)
#     contactProfessionnel = serializers.CharField(required=False, allow_blank=True)
#     etatCivil = serializers.IntegerField(required=False)
#     nombreEnfants = serializers.IntegerField(required=False)
#     # --- À METTRE EN HAUT AVEC LES AUTRES DÉCLARATIONS ---
#     date_embauche = serializers.DateField(required=False, allow_null=True)
#     fonction = serializers.CharField(required=False, allow_blank=True)
#     date_sortie = serializers.DateField(required=False, allow_null=True)
#     poste_superieur = serializers.CharField(required=False, allow_blank=True)
#     service_actuel = serializers.CharField(required=False, allow_blank=True)
#     financement_actuel = serializers.CharField(required=False, allow_blank=True)
#     num_contrat = serializers.CharField(required=False, allow_blank=True)
#     type_contrat = serializers.CharField(required=False, allow_blank=True)
#     photoContrat = serializers.FileField(required=False, allow_null=True)
#     photoUrl = serializers.FileField(required=False, allow_null=True)
#     cin = serializers.DictField(required=False, allow_null=True)
#     contrat = serializers.DictField(required=False, allow_null=True)
#     num_contrat = serializers.CharField(required=False, allow_blank=True)
#     type_contrat = serializers.CharField(required=False, allow_blank=True)
#     salaire = serializers.DecimalField(max_digits=15, decimal_places=2, required=False, allow_null=True)
#     periodeEssai = serializers.CharField(required=False, allow_blank=True)
#     dateFinEssai = serializers.DateField(required=False, allow_null=True)
#     photoContrat = serializers.FileField(required=False, allow_null=True)

#     # --- CHAMPS PARENTS & CONJOINT ---
#     nomPere = serializers.CharField(required=False, allow_blank=True)
#     nomMere = serializers.CharField(required=False, allow_blank=True)
#     nomConjoint = serializers.CharField(required=False, allow_blank=True)
#     prenomConjoint = serializers.CharField(required=False, allow_blank=True)
#     telConjoint = serializers.CharField(required=False, allow_blank=True)
#     emailConjoint = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
#     adresseConjoint = serializers.CharField(required=False, allow_blank=True)

#     # --- BANQUE ---
#     banque = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     agence = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     villeAgence = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     rib = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     photoRib = serializers.FileField(required=False, allow_null=True)

#     photoResidence = serializers.FileField(required=False, allow_null=True)
#     acteNaissance = serializers.FileField(required=False, allow_null=True)
#     casierjudiciaire = serializers.FileField(required=False, allow_null=True)

#     # --- AJOUT POUR LE CONJOINT (Acte de mariage) ---
#     acteMariage = serializers.FileField(required=False, allow_null=True)
    
#     # --- LISTES D'ACTIONS ---
#     ajouter_experiences = serializers.ListField(required=False)
#     mettre_a_jour_experiences = serializers.ListField(required=False)
#     supprimer_experiences = serializers.ListField(required=False)
#     ajouter_diplomes = serializers.ListField(required=False)
#     mettre_a_jour_diplomes = serializers.ListField(required=False)
#     supprimer_diplomes = serializers.ListField(required=False)
#     ajouter_formations = serializers.ListField(required=False)
#     mettre_a_jour_formations = serializers.ListField(required=False)
#     supprimer_formations = serializers.ListField(required=False)
#     ajouter_enfants = serializers.ListField(required=False)
#     mettre_a_jour_enfants = serializers.ListField(required=False)
#     supprimer_enfants = serializers.ListField(required=False)
#     ajouter_contacts_urgence = serializers.ListField(required=False)
#     mettre_a_jour_contacts_urgence = serializers.ListField(required=False)
#     supprimer_contacts_urgence = serializers.ListField(required=False)

#     class Meta:
#         model = Personnelles
#         fields = '__all__'

#     def _parse_json(self, data):
#         if not data: return []
#         try:
#             if isinstance(data, list) and len(data) > 0 and isinstance(data[0], str):
#                 return json.loads(data[0])
#             if isinstance(data, str): return json.loads(data)
#             return data
#         except: return []

#     def update(self, instance, validated_data):
#         # --- 1. EXTRACTION DES DONNÉES HORS-MODÈLE PRINCIPAL ---
#         nom_p = validated_data.pop('nomPere', None)
#         nom_m = validated_data.pop('nomMere', None)
#         nom_c = validated_data.pop('nomConjoint', None)
#         pre_c = validated_data.pop('prenomConjoint', None)
#         tel_c = validated_data.pop('telConjoint', None)
#         eml_c = validated_data.pop('emailConjoint', None)
#         adr_c = validated_data.pop('adresseConjoint', None)
#         a_mariage = validated_data.pop('acteMariage', None)
        
#         b_name = validated_data.pop('banque', None)
#         a_name = validated_data.pop('agence', None)
#         v_val = validated_data.pop('villeAgence', None)
#         r_val = validated_data.pop('rib', None)
#         p_rib = validated_data.pop('photoRib', None)
        
        
#         # Extraction CIN data additionnelle
#         d_duplicata = validated_data.pop('dateDuplicataCin', None)
#         l_duplicata = validated_data.pop('lieuDuplicataCin', None)
#         p_cin = validated_data.pop('photoCin', None)

#         photo_url = validated_data.pop('photoUrl', None)
#         cin_data = validated_data.pop('cin', None)           # objet cin complet
        
#         add_enf = self._parse_json(validated_data.pop('ajouter_enfants', []))
#         upd_enf = self._parse_json(validated_data.pop('mettre_a_jour_enfants', []))
#         del_enf = self._parse_json(validated_data.pop('supprimer_enfants', []))

#         add_con = self._parse_json(validated_data.pop('ajouter_contacts_urgence', []))
#         upd_con = self._parse_json(validated_data.pop('mettre_a_jour_contacts_urgence', []))
#         del_con = self._parse_json(validated_data.pop('supprimer_contacts_urgence', []))

#         p_residence = validated_data.pop('photoResidence', None)
#         a_naissance = validated_data.pop('acteNaissance', None)
#         c_judiciaire = validated_data.pop('casierjudiciaire', None)

#         # Champs Fonction
#         date_embauche = validated_data.pop('date_embauche', None)
#         date_sortie = validated_data.pop('date_sortie', None)
#         fonction_nom = validated_data.pop('fonction', None)
#         poste_nom = validated_data.pop('poste_superieur', None)
#         service_nom = validated_data.pop('service_actuel', None)
#         financement_nom = validated_data.pop('financement_actuel', None)

#         sexe_val = validated_data.pop('sexe', None)
#         if sexe_val:
#             instance.sexe = sexe_val if isinstance(sexe_val, Sexes) else Sexes.objects.get(id=sexe_val)

#         for attr, value in validated_data.items():
#             if not isinstance(value, (list, dict)):
#                 setattr(instance, attr, value)
        
#         if photo_url and not isinstance(photo_url, str):
#             instance.photo = photo_url   # ← change "photo" si ton champ s'appelle autrement

#         instance.save()

#         # --- 3. GESTION DES COORDONNÉES BANCAIRES ---
#         bank_obj, _ = CoordonneesBancaires.objects.get_or_create(personnelle=instance)
        
#         if b_name:
#             nom_banque = b_name.strip()
#             banque_inst = Banques.objects.filter(nom__iexact=nom_banque).first()
#             if not banque_inst:
#                 banque_inst = Banques.objects.create(nom=nom_banque)
#             bank_obj.banque = banque_inst

#         if a_name:
#             nom_agence = a_name.strip()
#             agence_inst = Agences.objects.filter(nom__iexact=nom_agence).first()
#             if not agence_inst:
#                 agence_inst = Agences.objects.create(nom=nom_agence, ville=v_val if v_val else "")
#             bank_obj.agence = agence_inst

#         if r_val is not None: bank_obj.rib = r_val
#         if p_rib and not isinstance(p_rib, str): bank_obj.photoRib = p_rib
#         bank_obj.save()

#         # --- 4. LOGIQUE ÉTAT CIVIL & FAMILLE ---
#         etat_civil_id = validated_data.get('etatCivil')
#         f_obj, _ = Famille.objects.get_or_create(personnelle=instance)
        
#         if nom_p is not None: f_obj.nomPere = nom_p
#         if nom_m is not None: f_obj.nomMere = nom_m

#         if str(etat_civil_id) == "2": # Marié
#             if nom_c is not None: f_obj.nomConjoint = nom_c
#             if pre_c is not None: f_obj.prenomConjoint = pre_c
#             if tel_c is not None: f_obj.telConjoint = tel_c
#             if eml_c is not None: f_obj.emailConjoint = eml_c
#             if adr_c is not None: f_obj.adresseConjoint = adr_c
#         else:
#             f_obj.nomConjoint = ""; f_obj.prenomConjoint = ""; f_obj.emailConjoint = None
#             a_mariage = validated_data.pop('acteMariage', None)
#         if a_mariage and not isinstance(a_mariage, str):
#             f_obj.acteMariage = a_mariage
#         f_obj.save()

#         # --- 5. GESTION DES ENFANTS ---
#         for item in add_enf:
#             item.pop('id', None)
#             s_id = item.pop('sexe', None)
#             Enfant.objects.create(personnelle=instance, sexe_id=s_id, **item)
#         for item in upd_enf:
#             eid = item.pop('id', None)
#             s_id = item.pop('sexe', None)
#             if eid:
#                 if s_id: item['sexe_id'] = s_id
#                 Enfant.objects.filter(id=eid, personnelle=instance).update(**item)
#         if del_enf: Enfant.objects.filter(id__in=del_enf, personnelle=instance).delete()

#         # --- 6. GESTION DES CONTACTS D'URGENCE ---
#         for item in add_con:
#             item.pop('id', None)
#             rel_id = item.pop('relation', None)
#             ContactUrgences.objects.create(personnelle=instance, relation_id=rel_id, **item)
#         for item in upd_con:
#             cid = item.pop('id', None)
#             rel_id = item.pop('relation', None)
#             if cid:
#                 if rel_id: item['relation_id'] = rel_id
#                 ContactUrgences.objects.filter(id=cid, personnelle=instance).update(**item)
#         if del_con: ContactUrgences.objects.filter(id__in=del_con, personnelle=instance).delete()

#         # --- 7. TABLES CIN ET PROPOS ---
#         cin_obj, _ = Cins.objects.get_or_create(personnelle=instance)

#         # 1. Données textuelles du CIN (reste inchangé)
#         if isinstance(cin_data, dict):
#             cin_obj.numeroCin = cin_data.get('numero') or cin_obj.numeroCin
#             cin_obj.dateCin = cin_data.get('dateDelivrance') or cin_obj.dateCin
#             cin_obj.lieuCin = cin_data.get('lieuDelivrance') or cin_obj.lieuCin
#             cin_obj.numeroDuplicata = cin_data.get('numeroDuplicata') or getattr(cin_obj, 'numeroDuplicata', '')
#             cin_obj.dateDuplicata = cin_data.get('dateDuplicata') or cin_obj.dateDuplicata
#             cin_obj.lieuDuplicata = cin_data.get('lieuDuplicata') or cin_obj.lieuDuplicata
#             cin_obj.save() # N'oublie pas de sauvegarder l'objet CIN

#         # 2. GESTION DE LA PHOTO (Dans la table Personnel / instance)
#         # On récupère la photo depuis validated_data
#         p_cin = validated_data.pop('cinphoto', None)

#         # On vérifie si c'est bien un fichier et non une simple string (URL)
#         if p_cin and not isinstance(p_cin, str):
#             # C'est ICI que ça change : on l'assigne à l'instance (Personnel)
#             instance.cinphoto = p_cin
#             instance.save() 
        
#         p_obj, _ = Propos.objects.get_or_create(personnelle=instance)

#         if p_residence and not isinstance(p_residence, str): 
#             instance.photoResidence = p_residence
#         if a_naissance and not isinstance(a_naissance, str): 
#             instance.acteNaissance = a_naissance
#         if c_judiciaire and not isinstance(c_judiciaire, str): 
#             instance.casierjudiciaire = c_judiciaire
#         instance.save()

#                 # ==================== CHAMPS FONCTION + RELATIONS ====================
#         date_embauche = validated_data.pop('date_embauche', None)
#         date_sortie = validated_data.pop('date_sortie', None)
#         fonction_nom = validated_data.pop('fonction', None)

#         # Service, Poste, Financement, Type Contrat → on récupère l'ID et on le transforme en objet
#         service_id = validated_data.pop('service_actuel', None)
#         poste_id = validated_data.pop('poste_superieur', None)
#         financement_id = validated_data.pop('financement_actuel', None)
#         type_contrat_id = validated_data.pop('type_contrat', None) or validated_data.pop('contrat_type', None)

#         # Mise à jour de la Fonction
#         f = Fonctions.objects.filter(personnelle=instance).last()
#         if not f:
#             f = Fonctions.objects.create(personnelle=instance)

#         if fonction_nom:
#             f.nom = fonction_nom

#         if service_id:
#             try:
#                 f.service = Services.objects.get(id=int(service_id))
#             except:
#                 pass

#         if poste_id:
#             try:
#                 f.poste = Postes.objects.get(id=int(poste_id))
#             except:
#                 pass

#         if financement_id:
#             try:
#                 f.financement = ModeFinancement.objects.get(id=int(financement_id))
#             except:
#                 pass

#         if date_embauche:
#             f.dateDebut = date_embauche
#         if date_sortie:
#             f.dateFin = date_sortie

#         f.save()

#         # ==================== CONTRAT (déjà corrigé précédemment) ====================
#         contrat_obj, _ = Contrat.objects.get_or_create(personnelle=instance)

#         if 'contrat_numero' in validated_data or 'num_contrat' in validated_data:
#             contrat_obj.NumeroContrat = validated_data.pop('contrat_numero', None) or validated_data.pop('num_contrat', None)

#         if type_contrat_id:
#             try:
#                 tc = TypeContrats.objects.get(id=int(type_contrat_id))
#                 contrat_obj.typeContrat = tc
#             except:
#                 pass

#         # Salaire, période, date fin essai...
#         salaire = validated_data.pop('contrat_salaire', validated_data.pop('salaire', None))
#         if salaire not in [None, '', 'null', 'None']:
#             try:
#                 contrat_obj.salaire = Decimal(str(salaire))
#             except:
#                 pass

#         contrat_obj.periodeEssai = validated_data.pop('contrat_periodeEssai', validated_data.pop('periodeEssai', contrat_obj.periodeEssai))
        
#         date_fin = validated_data.pop('contrat_dateFinEssai', validated_data.pop('dateFinEssai', None))
#         if date_fin not in [None, '', 'null', 'None']:
#             contrat_obj.dateFinEssai = date_fin

#         # Photo contrat
#         photo = validated_data.pop('photoContrat', None)
#         if photo and not isinstance(photo, str):
#             contrat_obj.photoContrat = photo

#         contrat_obj.save()

        

#         return instance