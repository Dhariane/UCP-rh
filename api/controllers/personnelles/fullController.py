from api.models.diplome.diplome import Diplome
from api.models.diplome.experience import Experience
from api.models.fonction.typeContrat import TypeContrats
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import json
from api.dto import PersonnellesDTO
from api.dto.fullpersonnelDto import PersonnelFullSerializer
from api.models.propos.enfant import Enfant
from api.models.propos.propos import Propos
from api.services.personnelles.propos import (
    CinsService, PersonnelleServices, EtatCivilService,
    PhotosService, ProposService,SexeService,EnfantService,FamilleService)
from api.services.personnelles.fonction import FonctionService, PosteService, ServiceService
from api.services.personnelles.fonction.contratService import ContratService
from api.services.personnelles.fonction.typeContrantService import TypeContratService
from api.services.personnelles.contact import ContactUrgencesService, RelationService
from api.services.personnelles.banque import CoordonneesBancaireServices, AgenceService, BanqueService
from api.services.personnelles.diplome.diplomeService import DiplomeService
from api.services.personnelles.diplome.experienceService import ExperienceService
from api.services.personnelles.diplome.formationService import FormationService
from api.services.personnelles.fonction.contratService import ContratService
from api.services.personnelles.fonction.typeContrantService import TypeContratService
from api.services.personnelles.fonction.modefinancementService import ModeFinancementService
from api.models import EtatCivil,Sexes,Relations,Postes,Personnelles,Services,ModeFinancement,Cins
from api.services.auth.login.loginService import  LoginService

class PersonnelFullController(APIView):
    renderer_classes = [JSONRenderer]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data
        # CAPI DES FICHIERS IMMÉDIATEMENT (Sécurité pour éviter les None)
        files = {k: v for k, v in request.FILES.items()}
        
        # Réinitialisation des curseurs de fichiers
        for f in files.values():
            f.seek(0)

        # Parsing JSON
        try:
            experiences = json.loads(data.get("experiences", "[]"))
            diplomes = json.loads(data.get("diplomes", "[]"))
            formations = json.loads(data.get("formations", "[]"))
            enfants = json.loads(data.get("enfants", "[]"))
        except Exception as e:
            return Response({"error": "Format JSON invalide"}, status=400)

        try:
            with transaction.atomic():
                # 1. Récupération des IDs depuis les données
                sexe_id = data.get("sexe")
                etat_civil_id = data.get("etatCivil")
                poste_id = data.get("poste")  # Peut être None ou une chaîne vide

                # On retire poste_id de la vérification obligatoire
                if not sexe_id or not etat_civil_id:
                    return Response({"error": "Sexe et Etat Civil sont obligatoires"}, status=400)

                # Récupération sécurisée des objets obligatoires
                try:
                    sexe = Sexes.objects.get(id=sexe_id)
                    etatcivil = EtatCivil.objects.get(id=etat_civil_id)
                    
                    # Récupération sécurisée des autres objets obligatoires
                    service = Services.objects.get(id=data.get("service"))
                    financement = ModeFinancement.objects.get(id=data.get("financement"))
                except (Sexes.DoesNotExist, Services.DoesNotExist, ModeFinancement.DoesNotExist) as e:
                    return Response({"error": f"Référence introuvable : {str(e)}"}, status=400)

                # --- LOGIQUE POUR LE POSTE OPTIONNEL ---
                poste = None
                if poste_id and poste_id not in ["", "null", "undefined"]:
                    try:
                        poste = Postes.objects.get(id=poste_id)
                    except Postes.DoesNotExist:
                        # Optionnel : décider si un mauvais ID de poste doit bloquer ou juste être ignoré
                        return Response({"error": "Le poste spécifié n'existe pas"}, status=400)

                # --- LOGIQUE TYPE CONTRAT (Ton code existant) ---
                type_contrat_id = data.get("typecontrat")
                if type_contrat_id:
                    try:
                        type_contrat = TypeContratService.get(type_contrat_id)
                    except Exception:
                        return Response({"error": "Type de contrat invalide"}, status=400)
                else:
                    return Response({"error": "Type de contrat requis"}, status=400)

                # 2. Banque et Agence
                banque = BanqueService.create({"nom": data.get("banque")})
                agence = AgenceService.create({
                    "nom": data.get("agence"),
                    "ville": data.get("villeAgence")
                })

                personnelles = PersonnelleServices.create({
                    "nom": data.get("nom"),
                    "prenom": data.get("prenom"),
                    "dateNaissance": data.get("dateNaissance"),
                    "lieuNaissance": data.get("lieuNaissance"),
                    "adresse": data.get("adresse"),
                    "emailPerso": data.get('emailPersonnel'),
                    "telPerso": data.get("telephonePersonnel"),
                    "quartier":data.get("quartier"),
                    "ville":data.get("ville"),
                    "sexe": sexe,
                    "photoResidence": files.get('photoresidence'),
                    "casierjudiciaire": files.get('photoCasier'),
                    "acteNaissance": files.get('photoacteNaissance'),
                    "cinphoto": files.get("photoCin")
                })
                # 4. CIN
                cin = CinsService.create({
                    "numeroCin": data.get("cin"),
                    "dateCin": data.get("dateDelivranceCin"),
                    "lieuCin": data.get("lieuDelivranceCin"),
                    "numeroDuplicata":data.get("numeroDuplicata"),
                    "dateDuplicata":data.get("dateDuplicata"),
                    "lieuDuplicata":data.get("lieuDuplicata"),
                    "personnelle": personnelles

                })

                # 5. Propos
                propos = ProposService.create({
                    "nif": data.get("nif"),
                    "stat": data.get("stat"),
                    "numeroCnaps": data.get("cnaps"),
                    "tel": data.get("contactProfessionnel"),
                    "email": data.get("emailProfessionnel"),
                    "nombreEnfant": data.get("nombreEnfants") or 0,
                    "etatCivil": etatcivil,
                    "personnelle": personnelles
                })
                # 3. Coordonnées bancaires
                coord = CoordonneesBancaireServices.create({
                    "rib": data.get("rib"),
                    "banque": banque,
                    "agence": agence,
                    "photo_rib": files.get('photoRibFile'),
                    "personnelle": personnelles.id
                })
                # Création du Contrat
                contrat = ContratService.create({
                    "NumeroContrat": data.get("NumeroContrat"),
                    "periodeEssai":data.get("periodeEssai"),
                    "dateFinEssai":data.get("dateFinEssai"),
                    "salaire":data.get("salaire"),
                    "photoContrat": files.get("photoContrat"),
                    "typeContrat": type_contrat,
                    "personnelle": personnelles
                })

                # 7. Contacts d'urgence
                if data.get("personne1"):
                    rel1 = Relations.objects.get(id=data.get("relation1"))
                    ContactUrgencesService.create({
                        "nom": data.get("personne1"),
                        "telephone": data.get("telephone1"),
                        "adresse": data.get("adresse1"),
                        "personnelle": personnelles,
                        "relation": rel1
                    })

                # Photo principale
                photo_file = files.get('photoFile')
                if photo_file:
                    PhotosService.create({
                        "nom": data.get("nom") + "_photo",
                        "data": photo_file,
                        "personnelle": personnelles.id
                    })

                if data.get("personne2"):
                    rel2 = Relations.objects.get(id=data.get("relation2"))
                    ContactUrgencesService.create({
                        "nom": data.get("personne2"),
                        "telephone": data.get("telephone2"),
                        "adresse": data.get("adresse2"),
                        "personnelle": personnelles,
                        "relation": rel2
                    })

                # 8. Fonction
                FonctionService.create({
                    "nom": data.get("fonction"),
                    "dateDebut": data.get("dateEmbauche"),
                    "dateFin": data.get("dateSortie") if data.get("dateSortie") else None,
                    "financement": financement,
                    "personnelle": personnelles,
                    "poste": poste,
                    "service": service,
                })

                # 9. Famille
                if data.get("nomPere") or data.get("nomMere"):
                    FamilleService.create({
                        "nomPere": data.get("nomPere"),
                        "nomMere": data.get("nomMere"),
                        "nomConjoint": data.get("nomConjoint"),
                        "prenomConjoint": data.get("prenomConjoint"),
                        "nombreEnfant": data.get("nombreEnfants") or 0,
                        "acteMariage": files.get("acteMariage"),
                        "telConjoint":data.get("telConjoint"),
                        "adresseConjoint":data.get("adresseConjoint"),
                        "emailConjoint":data.get("emailConjoint"),
                        "personnelle": personnelles
                    })

                # Expériences
                for exp in experiences:
                    ExperienceService.create({
                        "entreprise": exp.get("entreprise"),
                        "poste": exp.get("poste"),
                        "datedebut": exp.get("dateDebut"),
                        "datefin": exp.get("dateFin"),
                        "description": exp.get("description"),
                        "personnelle": personnelles.id
                    })

                # Diplômes
                for i, dip in enumerate(diplomes):
                    key = f"diplome_file_{i}"
                    DiplomeService.create({
                        "nom": dip.get("intitule"),
                        "etablissement": dip.get("etablissement"),
                        "dateObtention": dip.get("annee"),
                        "photo": files.get(key),
                        "personnelle": personnelles.id
                    })

                # Formations
                for i, form in enumerate(formations):
                    key = f"formation_file_{i}"
                    FormationService.create({
                        "titre": form.get("theme"),
                        "organisme": form.get("organisme"),
                        "lieu": form.get("lieu"),
                        "annee": form.get("annee"),
                        "attestation": files.get(key),
                        "personnelle": personnelles.id
                    })

                for i, enf in enumerate(enfants):
                    key = f"certificat_enfant_{i}" 
                    donnees_enfant = {
                        "nom": enf.get("nom"),
                        "prenom": enf.get("prenom"),
                        "dateNaissance": enf.get("dateNaissance"),
                        "lieuNaissance": enf.get("lieuNaissance"),
                        "personnelle": personnelles.id,
                        "sexe": sexe
                        
                    }
                    fichier_certificat = request.FILES.get(key)
                    if fichier_certificat:
                        donnees_enfant["certificatVie"] = fichier_certificat
                    EnfantService.create(donnees_enfant)

                LoginService.create(propos)

                return Response({"status": "success", 
                                 "message": "Personnel et accès créés avec succès Son Compte est creer et un email de notification a été envoyé"},
                                 status=201)

        except Exception as e:
            print("ERREUR CRITIQUE :", str(e))
            return Response({"error": str(e)}, status=400)

    def get(self, request, pk=None):
        try:
            if pk:
                # --- RÉCUPÉRATION D'UN SEUL PERSONNEL (POUR SON COMPTE) ---
                # On utilise prefetch_related pour charger toutes les listes en une seule fois
                personne = Personnelles.objects.prefetch_related(
                    'sexe', 'cins','propos_list','propos_list__etatCivil',
                    'Diplome', 'Experience', 'Enfant', 'contrat', 
                    'contrat__typeContrat', 'fonctions', 'fonctions__service', 
                    'fonctions__poste', 'contactUrgence', 'photos'
                ).get(pk=pk)
                
                # context={'request': request} permet d'avoir l'URL complète pour les images (http://...)
                serializer = PersonnelFullSerializer(personne, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
                # --- RÉCUPÉRATION DE TOUT LE PERSONNEL (POUR LA LISTE) ---
                personnes = Personnelles.objects.all().prefetch_related('sexe', 'fonctions__poste', 'fonctions__service')
                serializer = PersonnelFullSerializer(personnes, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Personnelles.DoesNotExist:
            return Response({"error": "Le personnel demandé n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    @transaction.atomic
    def put(self, request, pk):
        try:
            # 1. Récupération de l'instance principale avec verrouillage pour la transaction
            personne = Personnelles.objects.select_for_update().get(pk=pk)
            data = request.data
            files = request.FILES

            # --- 2. Mise à jour CIN (Cins) ---
            cin_lie = Cins.objects.filter(personnelle=personne).first()
            cin_vals = {
                "numeroCin": data.get('cin') or data.get('numeroCin'),
                "dateCin": data.get('dateDelivranceCin') or data.get('dateCin'),
                "lieuCin": data.get('lieuDelivranceCin') or data.get('lieuCin')
            }
            if cin_lie:
                for key, val in cin_vals.items():
                    if val: setattr(cin_lie, key, val)
                if 'photoCin' in files: cin_lie.photo = files['photoCin']
                cin_lie.save()
            else:
                Cins.objects.create(personnelle=personne, **cin_vals)

            # --- 3. Mise à jour des Propos (Infos sociales & RH) ---
            propos_lie = Propos.objects.filter(personnelle=personne).first()
            if propos_lie:
                propos_lie.numeroCnaps = data.get('cnaps') or data.get('numeroCnaps', propos_lie.numeroCnaps)
                propos_lie.nif = data.get('nif', propos_lie.nif)
                propos_lie.stat = data.get('stat', propos_lie.stat)
                propos_lie.tel = data.get('contactProfessionnel') or data.get('tel', propos_lie.tel)
                propos_lie.email = data.get('emailProfessionnel') or data.get('email', propos_lie.email)
                propos_lie.nombreEnfant = data.get('nombreEnfants') or data.get('nombreEnfant', propos_lie.nombreEnfant)
                if data.get('etatCivil'):
                    propos_lie.etatCivil_id = data.get('etatCivil')
                propos_lie.save()

            # --- 4. Mise à jour Coordonnées Bancaires ---
            from api.models.banque.coordonneesBancaires import CoordonneesBancaires # Vérifie ton import
            coord = CoordonneesBancaires.objects.filter(personnelle=personne).first()
            if coord:
                coord.rib = data.get('rib', coord.rib)
                if data.get('banque'): coord.banque_id = data.get('banque')
                if data.get('agence'): coord.agence_id = data.get('agence')
                if 'photoRibFile' in files: coord.photo_rib = files['photoRibFile']
                coord.save()

            # --- 5. Mise à jour de la Famille (Parents et Conjoint) ---
            from api.models.propos.famille import Famille
            famille_lie = Famille.objects.filter(personnelle=personne).first()
            famille_fields = [
                "nomPere", "prenomPere", "nomMere", "prenomMere", 
                "nomConjoint", "prenomConjoint", "telConjoint", 
                "adresseConjoint", "emailConjoint"
            ]
            if famille_lie:
                for field in famille_fields:
                    val = data.get(field)
                    if val is not None: setattr(famille_lie, field, val)
                if 'acteMariage' in files: famille_lie.acteMariage = files['acteMariage']
                famille_lie.save()

            # --- 6. Mise à jour du Personnel (Table principale) ---
            personne.nom = data.get('nom', personne.nom)
            personne.prenom = data.get('prenom', personne.prenom)
            personne.adresse = data.get('adresse', personne.adresse)
            personne.dateNaissance = data.get('dateNaissance', personne.dateNaissance)
            personne.lieuNaissance = data.get('lieuNaissance', personne.lieuNaissance)
            personne.emailPerso = data.get('emailPersonnel', personne.emailPerso)
            # Gestion flexible du téléphone
            personne.telPerso = data.get('telephonePersonnel') or data.get('telPerso') or personne.telPerso
            
            if data.get('sexe'): personne.sexe_id = data.get('sexe')
            
            # Fichiers scans directs sur Personnelles
            if 'photo' in files: personne.photos = files['photo']
            if 'photoresidence' in files: personne.photoResidence = files['photoresidence']
            if 'photoCasier' in files: personne.casierjudiciaire = files['photoCasier']
            if 'photoacteNaissance' in files: personne.acteNaissance = files['photoacteNaissance']
            
            personne.save()

            # DIPLÔMES
            # --- SECTION DIPLOMES ---
            if any(key.startswith('diplomes[') for key in data):
                # On récupère les diplômes déjà existants en base pour ce personnel
                existing_diplomes = {d.id: d for d in personne.Diplome.all()}
                received_ids = []
                i = 0
                
                while f'diplomes[{i}][nom]' in data:
                    d_id = data.get(f'diplomes[{i}][id]')
                    
                    # Nettoyage des valeurs (vide, "null", "undefined" -> None)
                    def get_clean_diplome(field):
                        v = data.get(f'diplomes[{i}][{field}]')
                        return v if v and str(v).strip() not in ["", "null", "undefined"] else None

                    d_vals = {
                        'nom': get_clean_diplome('nom'),
                        'etablissement': get_clean_diplome('etablissement'),
                        'dateObtention': get_clean_diplome('annee'), # Vérifie si c'est 'annee' ou 'dateObtention' dans ton FormData
                    }
                    
                    # Gestion du fichier (scan diplôme)
                    photo_file = files.get(f'diplomes[{i}][scan_diplome]')
                    if photo_file:
                        d_vals['photo'] = photo_file

                    if d_id and str(d_id).isdigit() and int(d_id) in existing_diplomes:
                        # --- UPDATE ---
                        obj = existing_diplomes[int(d_id)]
                        for key, val in d_vals.items():
                            if val is not None:
                                setattr(obj, key, val)
                        obj.save()
                        received_ids.append(int(d_id))
                    else:
                        # --- CREATE ---
                        # SÉCURITÉ : Vérifier les champs obligatoires pour un nouveau diplôme
                        if not d_vals['nom'] or not d_vals['etablissement']:
                            return Response(
                                {"error": f"Le nom et l'établissement sont obligatoires pour le diplôme à l'index {i}"},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                        
                        new_obj = Diplome.objects.create(
                            personnelle=personne, 
                            **{k:v for k,v in d_vals.items() if v is not None}
                        )
                        received_ids.append(new_obj.id)
                        
                    i += 1
                
                # Supprime les diplômes qui ne sont plus envoyés (ceux supprimés dans le front)
                personne.Diplome.exclude(id__in=received_ids).delete()

            # ENFANTS
            # --- Section ENFANTS ---
                if any(key.startswith('enfants[') for key in data):
                    existing_enfants = {e.id: e for e in personne.Enfant.all()}
                    received_ids = []
                    j = 0
                    
                    while f'enfants[{j}][nom]' in data:
                        e_id = data.get(f'enfants[{j}][id]')
                        
                        # --- NETTOYAGE STRICT ---
                        # On récupère la valeur brute et on s'assure que si c'est vide, ça devient None
                        def get_clean(field):
                            val = data.get(f'enfants[{j}][{field}]')
                            if val == "" or val == "null" or val == "undefined":
                                return None
                            return val

                        e_vals = {
                            'nom': get_clean('nom'),
                            'prenom': get_clean('prenom'),
                            'dateNaissance': get_clean('dateNaissance'),
                            'lieuNaissance': get_clean('lieuNaissance'),
                        }
                        
                        # Fichier certificat
                        certif_file = files.get(f'enfants[{j}][certificatFile]')
                        if certif_file:
                            e_vals['certificatVie'] = certif_file

                        # --- LOGIQUE UPDATE / CREATE ---
                        if e_id and str(e_id).isdigit() and int(e_id) in existing_enfants:
                            obj = existing_enfants[int(e_id)]
                            for key, val in e_vals.items():
                                if val is not None: # Si c'était vide, val est None, donc on n'y touche pas
                                    setattr(obj, key, val)
                            obj.save()
                            received_ids.append(int(e_id))
                        else:
                            # Pour un nouveau (CREATE), on enlève les None pour laisser le modèle
                            # soit prendre la valeur par défaut, soit lever une erreur propre
                            clean_new = {k: v for k, v in e_vals.items() if v is not None}
                            new_obj = Enfant.objects.create(personnelle=personne, **clean_new)
                            received_ids.append(new_obj.id)
                            
                        j += 1

                    personne.Enfant.exclude(id__in=received_ids).delete()

            # EXPÉRIENCES
            if any(key.startswith('experiences[') for key in data):
                existing_exps = {ex.id: ex for ex in personne.Experience.all()}
                received_ids = []
                k = 0
                
                while f'experiences[{k}][entreprise]' in data:
                    exp_id = data.get(f'experiences[{k}][id]')
                    exp_vals = {
                        'entreprise': data.get(f'experiences[{k}][entreprise]'),
                        'poste': data.get(f'experiences[{k}][poste]'),
                        'datedebut': data.get(f'experiences[{k}][datedebut]'),
                        'datefin': data.get(f'experiences[{k}][datefin]'),
                        'description': data.get(f'experiences[{k}][description]'),
                    }

                    if exp_id and str(exp_id).isdigit() and int(exp_id) in existing_exps:
                        # UPDATE
                        obj = existing_exps[int(exp_id)]
                        for key, val in exp_vals.items():
                            if val is not None:
                                setattr(obj, key, val)
                        obj.save()
                        received_ids.append(int(exp_id))
                    else:
                        # CREATE
                        clean_vals = {k: v for k, v in exp_vals.items() if v is not None}
                        new_obj = Experience.objects.create(personnelle=personne, **clean_vals)
                        received_ids.append(new_obj.id)
                    k += 1

                personne.Experience.exclude(id__in=received_ids).delete()

            # CONTACTS URGENCE (Gestion dynamique)
            if data.get('personne1'):
                # On nettoie les anciens contacts d'urgence avant de remettre les nouveaux
                from api.models.contact.contactUrgences import ContactUrgences
                ContactUrgences.objects.filter(personnelle=personne).delete()
                
                # Contact 1
                ContactUrgences.objects.create(
                    nom=data.get('personne1'),
                    telephone=data.get('telephone1'),
                    adresse=data.get('adresse1'),
                    relation_id=data.get('relation1'),
                    personnelle=personne
                )
                # Contact 2 (optionnel)
                if data.get('personne2'):
                    ContactUrgences.objects.create(
                        nom=data.get('personne2'),
                        telephone=data.get('telephone2'),
                        adresse=data.get('adresse2'),
                        relation_id=data.get('relation2'),
                        personnelle=personne
                    )

            # --- 8. RELOAD FINAL ---
            personne_updated = Personnelles.objects.prefetch_related(
                'sexe', 'cins', 'propos_list', 'Diplome', 'Enfant', 'Experience', 'contactUrgence'
            ).get(pk=pk)

            serializer = PersonnelFullSerializer(personne_updated, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Personnelles.DoesNotExist:
            return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Erreur critique PUT: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            personne = Personnelles.objects.get(pk=pk)
            # Pas besoin de supprimer le CIN ou le RIB à la main, 
            # le CASCADE s'en charge automatiquement !
            personne.delete() 
            return Response(
                {"message": f"Le personnel ID {pk} et toutes ses données liées ont été supprimés."}, 
                status=status.HTTP_204_NO_CONTENT
            )
        except Personnelles.DoesNotExist:
            return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)