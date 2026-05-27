from decimal import Decimal, InvalidOperation
import json

from rest_framework import serializers

from api.models.banque.agences import Agences
from api.models.banque.banques import Banques
from api.models.banque.coordonneesBancaires import CoordonneesBancaires
from api.models.contact.contactUrgences import ContactUrgences
from api.models.fonction.contrat import Contrat
from api.models.fonction.fonctions import Fonctions
from api.models.fonction.modefinancement import ModeFinancement
from api.models.fonction.poste import Postes
from api.models.fonction.service import Services
from api.models.fonction.typeContrat import TypeContrats
from api.models.propos.Cins import Cins
from api.models.propos.enfant import Enfant
from api.models.propos.famille import Famille
from api.models.propos.personnelles import Personnelles
from api.models.propos.propos import Propos
from api.models.propos.sexe import Sexes

try:
    from api.models.diplome.diplome import Diplome
    from api.models.diplome.formation import Formation
    from api.models.diplome.experience import Experience
    HAS_PARCOURS = True
except ImportError:
    HAS_PARCOURS = False

LIST_FIELDS = [
    'ajouter_enfants', 'mettre_a_jour_enfants', 'supprimer_enfants',
    'ajouter_contacts_urgence', 'mettre_a_jour_contacts_urgence', 'supprimer_contacts_urgence',
    'ajouter_experiences', 'mettre_a_jour_experiences', 'supprimer_experiences',
    'ajouter_diplomes', 'mettre_a_jour_diplomes', 'supprimer_diplomes',
    'ajouter_formations', 'mettre_a_jour_formations', 'supprimer_formations',
]


class PersonnelUpdateSerializer(serializers.ModelSerializer):

    # ── Infos personnelles ──────────────────────────────────
    emailPersonnel     = serializers.EmailField(source='emailPerso', required=False)
    telephonePersonnel = serializers.CharField(source='telPerso', required=False)
    num_cin_input      = serializers.CharField(required=False, allow_blank=True)
    dateDelivranceCin  = serializers.DateField(required=False, allow_null=True)
    lieuDelivranceCin  = serializers.CharField(required=False, allow_blank=True)
    dateDuplicataCin   = serializers.DateField(required=False, allow_null=True)
    lieuDuplicataCin   = serializers.CharField(required=False, allow_blank=True)
    photoCin           = serializers.FileField(required=False, allow_null=True)

    # ── Propos & Famille ────────────────────────────────────
    nif                  = serializers.CharField(required=False, allow_blank=True)
    stat                 = serializers.CharField(required=False, allow_blank=True)
    cnaps                = serializers.CharField(required=False, allow_blank=True)
    emailProfessionnel   = serializers.EmailField(required=False, allow_blank=True)
    contactProfessionnel = serializers.CharField(required=False, allow_blank=True)
    etatCivil            = serializers.IntegerField(required=False, allow_null=True)
    nombreEnfants        = serializers.IntegerField(required=False, allow_null=True)

    # ── Fonctions ───────────────────────────────────────────
    date_embauche      = serializers.DateField(required=False, allow_null=True)
    fonction           = serializers.CharField(required=False, allow_blank=True)
    date_sortie        = serializers.DateField(required=False, allow_null=True)
    poste_superieur    = serializers.CharField(required=False, allow_blank=True)
    service_actuel     = serializers.CharField(required=False, allow_blank=True)
    financement_actuel = serializers.CharField(required=False, allow_blank=True)

    # ── Contrat ─────────────────────────────────────────────
    num_contrat  = serializers.CharField(required=False, allow_blank=True)
    type_contrat = serializers.CharField(required=False, allow_blank=True)
    salaire      = serializers.DecimalField(max_digits=15, decimal_places=2, required=False, allow_null=True)
    periodeEssai = serializers.CharField(required=False, allow_blank=True)
    dateFinEssai = serializers.DateField(required=False, allow_null=True)
    photoContrat = serializers.FileField(required=False, allow_null=True)
    photoUrl     = serializers.FileField(required=False, allow_null=True)
    cin          = serializers.DictField(required=False, allow_null=True)
    contrat      = serializers.DictField(required=False, allow_null=True)

    # ── Parents & Conjoint ──────────────────────────────────
    nomPere         = serializers.CharField(required=False, allow_blank=True)
    nomMere         = serializers.CharField(required=False, allow_blank=True)
    nomConjoint     = serializers.CharField(required=False, allow_blank=True)
    prenomConjoint  = serializers.CharField(required=False, allow_blank=True)
    telConjoint     = serializers.CharField(required=False, allow_blank=True)
    emailConjoint   = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    adresseConjoint = serializers.CharField(required=False, allow_blank=True)
    acteMariage     = serializers.FileField(required=False, allow_null=True)

    # ── Banque ──────────────────────────────────────────────
    banque      = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    agence      = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    villeAgence = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    rib         = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    photoRib    = serializers.FileField(required=False, allow_null=True)

    # ── Documents ───────────────────────────────────────────
    photoResidence   = serializers.FileField(required=False, allow_null=True)
    acteNaissance    = serializers.FileField(required=False, allow_null=True)
    casierjudiciaire = serializers.FileField(required=False, allow_null=True)

    # ── Listes ──────────────────────────────────────────────
    ajouter_enfants                = serializers.ListField(required=False)
    mettre_a_jour_enfants          = serializers.ListField(required=False)
    supprimer_enfants              = serializers.ListField(required=False)
    ajouter_contacts_urgence       = serializers.ListField(required=False)
    mettre_a_jour_contacts_urgence = serializers.ListField(required=False)
    supprimer_contacts_urgence     = serializers.ListField(required=False)
    ajouter_experiences            = serializers.ListField(required=False)
    mettre_a_jour_experiences      = serializers.ListField(required=False)
    supprimer_experiences          = serializers.ListField(required=False)
    ajouter_diplomes               = serializers.ListField(required=False)
    mettre_a_jour_diplomes         = serializers.ListField(required=False)
    supprimer_diplomes             = serializers.ListField(required=False)
    ajouter_formations             = serializers.ListField(required=False)
    mettre_a_jour_formations       = serializers.ListField(required=False)
    supprimer_formations           = serializers.ListField(required=False)
    nombreAnneeExperience          = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model  = Personnelles
        fields = '__all__'

    # ── Helpers ──────────────────────────────────────────────
    def _safe_int(self, val):
        try:
            return int(str(val).strip())
        except (ValueError, TypeError):
            return None

    def _safe_date(self, val):
        if val in [None, '', 'null', 'None', 'undefined']:
            return None
        return val

    def _parse_json(self, data):
        if not data:
            return []
        try:
            if isinstance(data, list):
                if len(data) == 0:
                    return []
                # FormData → ["[{...}]"]
                if isinstance(data[0], str):
                    parsed = json.loads(data[0])
                else:
                    parsed = data
            elif isinstance(data, str):
                parsed = json.loads(data)
            else:
                parsed = data

            # Déplie [[{...}]] → [{...}]
            if isinstance(parsed, list) and len(parsed) == 1 and isinstance(parsed[0], list):
                parsed = parsed[0]

            return parsed if isinstance(parsed, list) else []
        except Exception:
            return []

    # ── Pré-traitement avant validation ──────────────────────
    def to_internal_value(self, data):
        data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Désérialiser les listes JSON
        for field in LIST_FIELDS:
            if field not in data:
                continue
            val = data[field]
            raw = val[0] if isinstance(val, list) and len(val) == 1 else val
            if isinstance(raw, str):
                try:
                    parsed = json.loads(raw)
                except (json.JSONDecodeError, TypeError):
                    parsed = []
            elif isinstance(raw, list):
                parsed = raw
            else:
                parsed = []
            # Déplie [[...]] → [...]
            if isinstance(parsed, list) and len(parsed) == 1 and isinstance(parsed[0], list):
                parsed = parsed[0]
            data[field] = parsed

        # Nettoyer les DateField vides
        for f in ['dateFinEssai', 'date_embauche', 'date_sortie', 'dateDelivranceCin', 'dateDuplicataCin']:
            if f in data:
                v = data[f]
                raw = v[0] if isinstance(v, list) and v else v
                if raw in ['', 'null', 'None', 'undefined']:
                    data[f] = None

        # Nettoyer etatCivil vide
        if 'etatCivil' in data:
            v = data['etatCivil']
            raw = v[0] if isinstance(v, list) and v else v
            if raw in ['', 'null', 'None', 'undefined']:
                data['etatCivil'] = None

        # Nettoyer emailConjoint vide
        if 'emailConjoint' in data:
            v = data['emailConjoint']
            raw = v[0] if isinstance(v, list) and v else v
            if raw in ['', 'null', 'None', 'undefined', 'NaN']:
                data['emailConjoint'] = None

        # Nettoyer salaire vide
        if 'salaire' in data:
            v = data['salaire']
            raw = v[0] if isinstance(v, list) and v else v
            if raw in ['', 'null', 'None', 'undefined']:
                data['salaire'] = None

        # Parser cin si c'est une string JSON
        if 'cin' in data:
            v = data['cin']
            raw = v[0] if isinstance(v, list) and v else v
            if isinstance(raw, str):
                try:
                    data['cin'] = json.loads(raw)
                except (json.JSONDecodeError, TypeError):
                    data['cin'] = None

        return super().to_internal_value(data)

    # ── Update principal ─────────────────────────────────────
    def update(self, instance, validated_data):

        # ── EXTRACTION FAMILLE ──────────────────────────────
        nom_p     = validated_data.pop('nomPere', None)
        nom_m     = validated_data.pop('nomMere', None)
        nom_c     = validated_data.pop('nomConjoint', None)
        pre_c     = validated_data.pop('prenomConjoint', None)
        tel_c     = validated_data.pop('telConjoint', None)
        eml_c     = validated_data.pop('emailConjoint', None)
        adr_c     = validated_data.pop('adresseConjoint', None)
        a_mariage = validated_data.pop('acteMariage', None)

        # ── EXTRACTION BANQUE ───────────────────────────────
        b_name = validated_data.pop('banque', None)
        a_name = validated_data.pop('agence', None)
        v_val  = validated_data.pop('villeAgence', None)
        r_val  = validated_data.pop('rib', None)
        p_rib  = validated_data.pop('photoRib', None)

        # ── EXTRACTION CIN ──────────────────────────────────
        date_delivrance_cin = validated_data.pop('dateDelivranceCin', None)
        lieu_delivrance_cin = validated_data.pop('lieuDelivranceCin', None)
        date_duplicata_cin  = validated_data.pop('dateDuplicataCin', None)
        lieu_duplicata_cin  = validated_data.pop('lieuDuplicataCin', None)
        num_cin_input       = validated_data.pop('num_cin_input', None)
        cin_data            = validated_data.pop('cin', None)
        validated_data.pop('photoCin', None)

        # ── EXTRACTION LISTES ───────────────────────────────
        add_enf = self._parse_json(validated_data.pop('ajouter_enfants', []))
        upd_enf = self._parse_json(validated_data.pop('mettre_a_jour_enfants', []))
        del_enf = self._parse_json(validated_data.pop('supprimer_enfants', []))

        add_con = self._parse_json(validated_data.pop('ajouter_contacts_urgence', []))
        upd_con = self._parse_json(validated_data.pop('mettre_a_jour_contacts_urgence', []))
        del_con = self._parse_json(validated_data.pop('supprimer_contacts_urgence', []))

        add_exp = self._parse_json(validated_data.pop('ajouter_experiences', []))
        upd_exp = self._parse_json(validated_data.pop('mettre_a_jour_experiences', []))
        del_exp = self._parse_json(validated_data.pop('supprimer_experiences', []))
        add_dip = self._parse_json(validated_data.pop('ajouter_diplomes', []))
        upd_dip = self._parse_json(validated_data.pop('mettre_a_jour_diplomes', []))
        del_dip = self._parse_json(validated_data.pop('supprimer_diplomes', []))
        add_for = self._parse_json(validated_data.pop('ajouter_formations', []))
        upd_for = self._parse_json(validated_data.pop('mettre_a_jour_formations', []))
        del_for = self._parse_json(validated_data.pop('supprimer_formations', []))
        validated_data.pop('nombreAnneeExperience', None)

        # ── EXTRACTION DOCUMENTS ────────────────────────────
        p_residence  = validated_data.pop('photoResidence', None)
        a_naissance  = validated_data.pop('acteNaissance', None)
        c_judiciaire = validated_data.pop('casierjudiciaire', None)

        # ── EXTRACTION FONCTIONS ────────────────────────────
        date_embauche   = self._safe_date(validated_data.pop('date_embauche', None))
        date_sortie     = self._safe_date(validated_data.pop('date_sortie', None))
        fonction_nom    = validated_data.pop('fonction', None)
        poste_nom       = validated_data.pop('poste_superieur', None)
        service_nom     = validated_data.pop('service_actuel', None)
        financement_nom = validated_data.pop('financement_actuel', None)

        # ── EXTRACTION CONTRAT ──────────────────────────────
        num_contrat     = validated_data.pop('num_contrat', None)
        type_contrat_id = validated_data.pop('type_contrat', None)
        salaire         = validated_data.pop('salaire', None)
        periode_essai   = validated_data.pop('periodeEssai', None)
        date_fin_essai  = self._safe_date(validated_data.pop('dateFinEssai', None))
        photo_contrat   = validated_data.pop('photoContrat', None)
        validated_data.pop('contrat', None)
        photo_url = validated_data.pop('photoUrl', None)

        # etatCivil : lu avant la boucle setattr
        etat_civil_id = validated_data.get('etatCivil')

        # ── SEXE ────────────────────────────────────────────
        sexe_val = validated_data.pop('sexe', None)
        if sexe_val:
            try:
                instance.sexe = (
                    sexe_val if isinstance(sexe_val, Sexes)
                    else Sexes.objects.get(id=int(sexe_val))
                )
            except Exception:
                pass

        # ── CHAMPS SIMPLES ────────────────────────────────────
        for attr, value in validated_data.items():
            if not isinstance(value, (list, dict)):
                setattr(instance, attr, value)

        instance.save()

        # ── PHOTO PROFIL ──────────────────────────────────────
        if photo_url and not isinstance(photo_url, str):
            from api.models.propos.photos import Photos
            photo_obj = instance.photos.first()
            if photo_obj:
                photo_obj.data = photo_url
                photo_obj.save()
            else:
                Photos.objects.create(personnelle=instance, data=photo_url)

        # ── BANQUE ──────────────────────────────────────────
        bank_obj, _ = CoordonneesBancaires.objects.get_or_create(personnelle=instance)
        if b_name:
            nom_banque  = str(b_name).strip()
            banque_inst = Banques.objects.filter(nom__iexact=nom_banque).first()
            if not banque_inst:
                banque_inst = Banques.objects.create(nom=nom_banque)
            bank_obj.banque = banque_inst
        if a_name:
            nom_agence  = str(a_name).strip()
            agence_inst = Agences.objects.filter(nom__iexact=nom_agence).first()
            if not agence_inst:
                agence_inst = Agences.objects.create(nom=nom_agence, ville=v_val or '')
            bank_obj.agence = agence_inst
        if r_val is not None: bank_obj.rib = r_val
        if p_rib and not isinstance(p_rib, str): bank_obj.photoRib = p_rib
        bank_obj.save()

        # ── FAMILLE & CONJOINT ──────────────────────────────
        f_obj, _ = Famille.objects.get_or_create(personnelle=instance)
        if nom_p is not None: f_obj.nomPere = nom_p
        if nom_m is not None: f_obj.nomMere = nom_m

        if self._safe_int(etat_civil_id) == 2:  # Marié(e)
            if nom_c is not None: f_obj.nomConjoint     = nom_c
            if pre_c is not None: f_obj.prenomConjoint  = pre_c
            if tel_c is not None: f_obj.telConjoint     = tel_c
            if eml_c is not None: f_obj.emailConjoint   = eml_c
            if adr_c is not None: f_obj.adresseConjoint = adr_c
            if a_mariage and not isinstance(a_mariage, str):
                f_obj.acteMariage = a_mariage
        else:
            f_obj.nomConjoint    = ''
            f_obj.prenomConjoint = ''
            f_obj.telConjoint    = ''
            f_obj.emailConjoint  = None
            f_obj.adresseConjoint= ''
        f_obj.save()

        # ── ENFANTS ─────────────────────────────────────────
        for item in add_enf:
            item = dict(item)
            item.pop('id', None)
            s_id = self._safe_int(item.pop('sexe', None))
            item.pop('certificatVie', None)
            try:
                Enfant.objects.create(personnelle=instance, sexe_id=s_id, **item)
            except Exception as e:
                print(f"Erreur création enfant: {e}")
        # ── CERTIFICATS DE VIE ENFANTS ──────────────────────────
            request = self.context.get('request')
            if request:
                for key, file in request.FILES.items():
                    # Front envoie certificatVie_0, certificatVie_1, ...
                    if not key.startswith('certificatVie_'):
                        continue
                    suffix = key.replace('certificatVie_', '')
                    # Ignorer certificatVie_index_X
                    if suffix.startswith('index_'):
                        continue
                    try:
                        index = int(suffix)
                    except ValueError:
                        continue
                    # Récupérer l'ID enfant associé
                    enfant_id_str = request.data.get(f'certificatVie_index_{index}', '')
                    try:
                        enfant_id = int(enfant_id_str)
                        enfant = Enfant.objects.filter(id=enfant_id, personnelle=instance).first()
                        if enfant:
                            enfant.certificatVie = file
                            enfant.save(update_fields=['certificatVie'])
                    except (ValueError, TypeError):
                        pass

        for item in upd_enf:
            item = dict(item)
            eid  = self._safe_int(item.pop('id', None))
            s_id = self._safe_int(item.pop('sexe', None))
            item.pop('certificatVie', None)
            if eid:
                if s_id: item['sexe_id'] = s_id
                try:
                    Enfant.objects.filter(id=eid, personnelle=instance).update(**item)
                except Exception as e:
                    print(f"Erreur MAJ enfant {eid}: {e}")

        if del_enf:
            Enfant.objects.filter(
                id__in=[self._safe_int(i) for i in del_enf],
                personnelle=instance
            ).delete()

        # ── CONTACTS D'URGENCE ──────────────────────────────
        for item in add_con:
            item = dict(item)
            item.pop('id', None)
            rel_id = self._safe_int(item.pop('relation', None))
            try:
                ContactUrgences.objects.create(personnelle=instance, relation_id=rel_id, **item)
            except Exception as e:
                print(f"Erreur création contact: {e}")

        for item in upd_con:
            item = dict(item)
            cid    = self._safe_int(item.pop('id', None))
            rel_id = self._safe_int(item.pop('relation', None))
            if cid:
                if rel_id: item['relation_id'] = rel_id
                try:
                    ContactUrgences.objects.filter(id=cid, personnelle=instance).update(**item)
                except Exception as e:
                    print(f"Erreur MAJ contact {cid}: {e}")

        if del_con:
            ContactUrgences.objects.filter(
                id__in=[self._safe_int(i) for i in del_con],
                personnelle=instance
            ).delete()

        # ── CIN ─────────────────────────────────────────────
        cin_obj, _ = Cins.objects.get_or_create(personnelle=instance)
        if num_cin_input:       cin_obj.numeroCin     = num_cin_input
        if date_delivrance_cin: cin_obj.dateCin       = date_delivrance_cin
        if lieu_delivrance_cin: cin_obj.lieuCin       = lieu_delivrance_cin
        if date_duplicata_cin:  cin_obj.dateDuplicata = date_duplicata_cin
        if lieu_duplicata_cin:  cin_obj.lieuDuplicata = lieu_duplicata_cin
        cin_obj.save()

        # ── PHOTO CIN ───────────────────────────────────────
        cinphoto = validated_data.pop('cinphoto', None)
        if cinphoto and not isinstance(cinphoto, str):
            instance.cinphoto = cinphoto
            instance.save()

        # ── DOCUMENTS ───────────────────────────────────────
        Propos.objects.get_or_create(personnelle=instance)
        if p_residence  and not isinstance(p_residence,  str): instance.photoResidence  = p_residence
        if a_naissance  and not isinstance(a_naissance,  str): instance.acteNaissance   = a_naissance
        if c_judiciaire and not isinstance(c_judiciaire, str): instance.casierjudiciaire= c_judiciaire
        instance.save()
        # ── FONCTIONS & CONTRAT ───────────────────────────────────────
        # ✅ Tout passe par Contrat maintenant
        from api.models.fonction.contrat import Contrat as ContratModel
        from api.models.fonction.fonctions import Fonctions as FonctionsModel

        contrat_obj, _ = ContratModel.objects.get_or_create(personnelle=instance)

        # Fonction
        if fonction_nom:
            fid = self._safe_int(fonction_nom)
            if fid:
                fonction_inst = FonctionsModel.objects.filter(id=fid).first()
            else:
                fonction_inst = FonctionsModel.objects.filter(
                    nom__iexact=str(fonction_nom).strip()
                ).first()
            if fonction_inst:
                contrat_obj.fonction = fonction_inst

        # Service
        if service_nom:
            sid = self._safe_int(service_nom)
            obj = Services.objects.filter(id=sid).first() if sid else \
                Services.objects.filter(nom__iexact=str(service_nom).strip()).first()
            if obj:
                contrat_obj.service = obj

        # Financement
        if financement_nom:
            fid = self._safe_int(financement_nom)
            obj = ModeFinancement.objects.filter(id=fid).first() if fid else \
                ModeFinancement.objects.filter(nom__iexact=str(financement_nom).strip()).first()
            if obj:
                contrat_obj.financement = obj

        # Dates
        if date_embauche: contrat_obj.dateDebut = date_embauche
        if date_sortie:   contrat_obj.dateFin   = date_sortie

        # Autres champs contrat
        if num_contrat:    contrat_obj.NumeroContrat = num_contrat
        if periode_essai:  contrat_obj.periodeEssai  = periode_essai
        if date_fin_essai: contrat_obj.dateFinEssai  = date_fin_essai

        if type_contrat_id:
            tc_id = self._safe_int(type_contrat_id)
            if tc_id:
                tc = TypeContrats.objects.filter(id=tc_id).first()
            else:
                tc = TypeContrats.objects.filter(
                    TypeContrat__iexact=str(type_contrat_id).strip()
                ).first()
            if tc:
                contrat_obj.typeContrat = tc

        if salaire not in [None, '', 'null', 'None']:
            try:
                contrat_obj.salaire = Decimal(str(salaire))
            except InvalidOperation:
                pass

        if photo_contrat and not isinstance(photo_contrat, str):
            contrat_obj.photoContrat = photo_contrat

        contrat_obj.save()

        # ── EXPÉRIENCES / DIPLÔMES / FORMATIONS ─────────────
        if HAS_PARCOURS:
            for item in add_exp:
                item = dict(item); item.pop('id', None); item.pop('isCurrent', None)
                try: Experience.objects.create(personnelle=instance, **item)
                except Exception as e: print(f"Erreur création expérience: {e}")

            for item in upd_exp:
                item = dict(item)
                eid = self._safe_int(item.pop('id', None)); item.pop('isCurrent', None)
                if eid:
                    try: Experience.objects.filter(id=eid, personnelle=instance).update(**item)
                    except Exception as e: print(f"Erreur MAJ expérience {eid}: {e}")

            if del_exp:
                Experience.objects.filter(
                    id__in=[self._safe_int(i) for i in del_exp], personnelle=instance
                ).delete()

            # ── DIPLÔMES ─────────────────────────────────────────
        from api.models.diplome.typeDiplome import DiplomeType  # ✅ ajouter cet import

        request = self.context.get('request')

        for item in add_dip:
            item = dict(item)
            item.pop('id', None)
            item.pop('fichier', None)

            # ✅ Extraire et résoudre type_diplome
            type_dip_id = item.pop('type_diplome', None)
            type_dip = None
            if type_dip_id:
                try:
                    type_dip = DiplomeType.objects.get(id=int(type_dip_id))
                except (DiplomeType.DoesNotExist, ValueError, TypeError):
                    pass

            # ✅ Extraire et convertir annee → anneeObtention
            annee_raw = item.pop('annee', None) or item.pop('dateObtention', None)
            annee_int = None
            if annee_raw:
                try:
                    annee_int = int(str(annee_raw)[:4])
                except (ValueError, TypeError):
                    pass

            try:
                Diplome.objects.create(
                    personnelle    = instance,
                    type_diplome   = type_dip,
                    filiere        = item.get('filiere', ''),
                    lieu           = item.get('lieu', ''),
                    etablissement  = item.get('etablissement', ''),
                    anneeObtention = annee_int,
                )
            except Exception as e:
                print(f"Erreur création diplôme: {e}")

            # ✅ Photos diplômes
            if request:
                for key, file in request.FILES.items():
                    if not key.startswith('diplome_photo_'):
                        continue
                    try:
                        index = int(key.replace('diplome_photo_', ''))
                        diplome_id_str = request.data.get(f'diplome_id_{index}', '')
                        diplome_id = int(diplome_id_str)
                        dip = Diplome.objects.filter(id=diplome_id, personnelle=instance).first()
                        if dip:
                            dip.photo = file
                            dip.save(update_fields=['photo'])
                    except (ValueError, TypeError):
                        pass

            for item in upd_dip:
                item = dict(item)
                did = self._safe_int(item.pop('id', None))
                item.pop('fichier', None)

                # ✅ Résoudre type_diplome
                type_dip_id = item.pop('type_diplome', None)
                if type_dip_id:
                    try:
                        item['type_diplome_id'] = int(type_dip_id)
                    except (ValueError, TypeError):
                        pass

        # ✅ Convertir annee → anneeObtention
        annee_raw = item.pop('annee', None) or item.pop('dateObtention', None)
        if annee_raw:
            try:
                item['anneeObtention'] = int(str(annee_raw)[:4])
            except (ValueError, TypeError):
                pass

        if did:
            try:
                Diplome.objects.filter(id=did, personnelle=instance).update(**item)
            except Exception as e:
                print(f"Erreur MAJ diplôme {did}: {e}")

            for item in add_for:
                item = dict(item)
                item.pop('id', None)
                item.pop('certificat', None)  # "certificat" est le nom frontend, pas le champ modèle
                try:
                    Formation.objects.create(personnelle=instance, **item)
                except Exception as e:
                    print(f"Erreur création formation: {e}")

            # ✅ Associer les attestations
            if request:
                for key, file in request.FILES.items():
                    if not key.startswith('formation_attestation_'):
                        continue
                    try:
                        index = int(key.replace('formation_attestation_', ''))
                        formation_id_str = request.data.get(f'formation_id_{index}', '')
                        formation_id = int(formation_id_str)
                        form = Formation.objects.filter(id=formation_id, personnelle=instance).first()
                        if form:
                            form.attestation = file  # ← "attestation" est le vrai nom du champ
                            form.save(update_fields=['attestation'])
                    except (ValueError, TypeError):
                        pass

            for item in upd_for:
                item = dict(item)
                fid = self._safe_int(item.pop('id', None))
                item.pop('certificat', None)
                if fid:
                    try:
                        Formation.objects.filter(id=fid, personnelle=instance).update(**item)
                    except Exception as e:
                        print(f"Erreur MAJ formation {fid}: {e}")
                    # ── NIF / STAT / CNAPS — stockés dans Propos ────────────
                        p_obj, _ = Propos.objects.get_or_create(personnelle=instance)
                        nif_val  = validated_data.get('nif')
                        stat_val = validated_data.get('stat')
                        cnaps_val= validated_data.get('cnaps')
                        if nif_val  is not None: p_obj.nif  = nif_val
                        if stat_val is not None: p_obj.stat = stat_val
                        if cnaps_val is not None: p_obj.cnaps = cnaps_val
                        p_obj.save()
        print(f"DEBUG validated_data restant: {list(validated_data.keys())}")
        print(f"DEBUG nif: {validated_data.get('nif')}")
        print(f"DEBUG stat: {validated_data.get('stat')}")

        return instance
