from argparse import Action

from api.models.diplome.diplome import Diplome
from api.models.diplome.experience import Experience
from api.models.diplome.typeDiplome import DiplomeType
from api.models.fonction.contrat import Contrat
from api.models.fonction.typeContrat import TypeContrats
from api.models.fonction.fonctions import Fonctions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
import json
from api.dto import PersonnellesDTO
from api.dto.fullpersonnelDto import PersonnelFullSerializer
from api.dto.fullUpdatePersonnelDto import PersonnelUpdateSerializer
from api.models.propos.enfant import Enfant
from api.models.propos.propos import Propos
from api.models.fonction.fonctions import Fonctions as FonctionsModel
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
from api.models import EtatCivil,Sexes,Relations,Postes,Personnelles,Services,ModeFinancement,Cins, fonction
from api.services.auth.login.loginService import  LoginService
from django.db.models import Prefetch

class PersonnelFullController(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def post(self, request):
        data = request.data
        # CAPI DES FICHIERS IMMÉDIATEMENT (Sécurité pour éviter les None)
        files = {k: v for k, v in request.FILES.items()}
        
        # Réinitialisation des curseurs de fichiers
        for f in files.values():
            f.seek(0)

        # Parsing JSON
        try:
            import json as json_module  # ← renommer pour éviter le conflit
            
            raw_exp  = data.get("experiences", "[]")
            raw_dip  = data.get("diplomes", "[]")
            raw_form = data.get("formations", "[]")
            raw_enf  = data.get("enfants", "[]")

            experiences = raw_exp  if isinstance(raw_exp,  list) else json_module.loads(raw_exp  or "[]")
            diplomes    = raw_dip  if isinstance(raw_dip,  list) else json_module.loads(raw_dip  or "[]")
            formations  = raw_form if isinstance(raw_form, list) else json_module.loads(raw_form or "[]")
            enfants     = raw_enf  if isinstance(raw_enf,  list) else json_module.loads(raw_enf  or "[]")

        except Exception as e:
            return Response({"error": f"Format JSON invalide : {str(e)}"}, status=400)

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
                fonction_obj = FonctionsModel.objects.get(id=data.get("fonction"))

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
                    "dateDuplicata":data.get("dateDuplicataCin"),
                    "lieuDuplicata":data.get("lieuDuplicataCin"),
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
                    "salaire":data.get("honoraire"),
                    "photoContrat": files.get("photoContrat"),
                    "typeContrat": type_contrat,
                    "personnelle": personnelles,
                    "fonction": fonction_obj,  
                    "service": service,        
                    "dateDebut": data.get("dateEmbauche"),
                    "dateFin": data.get("dateSortie") or None,
                    "financement": financement
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
                
                superieurs_ids = data.get("superieurs", "[]")
                if isinstance(superieurs_ids, str):
                    import json
                    superieurs_ids = json.loads(superieurs_ids)

                if superieurs_ids:
                    from api.models.auth.login.loginModel import Login
                    for login_id in superieurs_ids:
                        try:
                            login_superieur = Login.objects.get(id=login_id)
                            fonction.superieurs.add(login_superieur)
                        except Login.DoesNotExist:
                            pass

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

                # ── Diplômes ✅ ───────────────────────────────────────
                for i, dip in enumerate(diplomes):
                    key         = f"diplome_file_{i}"
                    type_dip_id = dip.get("type_diplome")

                    DiplomeService.create({
                        "type_diplome":  type_dip_id,        # ✅ ID directement, pas l'objet
                        "filiere":       dip.get("filiere"),
                        "lieu":          dip.get("lieu"),
                        "etablissement": dip.get("etablissement"),
                        "annneObtention": dip.get("annee"),   # ✅ attention au nom du champ
                        "photo":         files.get(key),
                        "personnelle":   personnelles.id
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
                        "sexe": sexe.id
                        
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

    from django.db.models import Prefetch

    def get(self, request, pk=None):
        try:
            if pk:
                # Utilisez Prefetch pour le chemin complexe
                personne = Personnelles.objects.prefetch_related(
                    'sexe', 
                    'cins', 
                    'propos_list', 
                    'propos_list__etatCivil',
                    'diplomes', 
                    'Experience', 
                    'Enfant', 
                    'contactUrgence', 
                    'photos',
                    # On précharge les contrats, et pour chaque contrat, on récupère la fonction liée
                    Prefetch(
                        'contrats', # Utilisation du related_name défini dans votre modèle
                        queryset=Contrat.objects.select_related('fonction', 'typeContrat', 'service', 'financement')
                    )
                ).get(pk=pk)
                
                serializer = PersonnelFullSerializer(personne, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            else:
            # CORRECTION ICI : Utilisez 'contrats' (le related_name) et non 'contrat__fonction'
                personnes = Personnelles.objects.all().prefetch_related(
                    'sexe',
                    Prefetch(
                        'contrats', # Utiliser le nom exact du related_name
                        queryset=Contrat.objects.select_related('fonction', 'typeContrat', 'service', 'financement')
                    )
                )
                serializer = PersonnelFullSerializer(personnes, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Personnelles.DoesNotExist:
            return Response({"error": "Le personnel demandé n'existe pas."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Erreur serveur: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def put(self, request, pk):
        try:
            # 1. Récupération de l'instance principale
            personne = Personnelles.objects.select_for_update().get(pk=pk)
            data = request.data
            files = request.FILES

            from api.models.fonction.contrat import Contrat
            contrat_lie = Contrat.objects.filter(personnelle=personne).first()
            if contrat_lie:
                # Mise à jour des champs du contrat
                contrat_lie.NumeroContrat = data.get('NumeroContrat', contrat_lie.NumeroContrat)
                contrat_lie.salaire = data.get('honoraire', contrat_lie.salaire)
                contrat_lie.dateDebut = data.get('dateEmbauche', contrat_lie.dateDebut)
                contrat_lie.dateFin = data.get('dateSortie', contrat_lie.dateFin)
                
                if data.get('service'): contrat_lie.service_id = data.get('service')
                if data.get('typecontrat'): contrat_lie.typeContrat_id = data.get('typecontrat')
                if data.get('financement'): contrat_lie.financement_id = data.get('financement')
                if 'photoContrat' in files: contrat_lie.photoContrat = files['photoContrat']
                
                contrat_lie.save()

            # --- 2. Mise à jour CIN (Cins) ---
            cin_lie = Cins.objects.filter(personnelle=personne).first()
            # HARMONISATION : On utilise num_cin_input (ce qui vient du front)
            cin_vals = {
                "numeroCin": data.get('num_cin_input') or data.get('cin'),
                "dateCin": data.get('dateDelivranceCin'),
                "lieuCin": data.get('lieuDelivranceCin')
            }
            if cin_lie:
                for key, val in cin_vals.items():
                    if val is not None: setattr(cin_lie, key, val)
                if 'photoCin' in files: cin_lie.photo = files['photoCin']
                cin_lie.save()
            else:
                Cins.objects.create(personnelle=personne, **cin_vals)

            # --- 3. Mise à jour des Propos (Infos sociales & RH) ---
            propos_lie = Propos.objects.filter(personnelle=personne).first()
            if propos_lie:
                propos_lie.numeroCnaps = data.get('cnaps') or propos_lie.numeroCnaps
                propos_lie.nif = data.get('nif') or propos_lie.nif
                propos_lie.stat = data.get('stat') or propos_lie.stat
                # HARMONISATION : correspond au FormData.append('telephonePersonnel')
                propos_lie.tel = data.get('telephonePersonnel') or propos_lie.tel
                propos_lie.email = data.get('emailPersonnel') or propos_lie.email
                propos_lie.nombreEnfant = data.get('nombreEnfants') or propos_lie.nombreEnfant
                if data.get('etatCivil'):
                    propos_lie.etatCivil_id = data.get('etatCivil')
                propos_lie.save()

            # --- 4. Mise à jour Coordonnées Bancaires ---
            # (Garde ton import ici s'il est nécessaire)
            from api.models.banque.coordonneesBancaires import CoordonneesBancaires
            coord = CoordonneesBancaires.objects.filter(personnelle=personne).first()
            if coord:
                coord.rib = data.get('rib') or coord.rib
                if data.get('banque'): coord.banque_id = data.get('banque')
                if data.get('agence'): coord.agence_id = data.get('agence')
                if 'photoRibFile' in files: coord.photo_rib = files['photoRibFile']
                coord.save()

            # --- 5. Mise à jour de la Famille ---
            from api.models.propos.famille import Famille
            famille_lie = Famille.objects.filter(personnelle=personne).first()
            if famille_lie:
                famille_fields = [
                    "nomPere", "prenomPere", "nomMere", "prenomMere", 
                    "nomConjoint", "prenomConjoint", "telConjoint", 
                    "adresseConjoint", "emailConjoint"
                ]
                for field in famille_fields:
                    val = data.get(field)
                    if val is not None: setattr(famille_lie, field, val)
                famille_lie.save()

            # --- 6. Mise à jour du Personnel (Table principale) ---
            personne.nom = data.get('nom', personne.nom)
            personne.prenom = data.get('prenom', personne.prenom)
            personne.adresse = data.get('adresse', personne.adresse)
            personne.dateNaissance = data.get('dateNaissance', personne.dateNaissance)
            personne.lieuNaissance = data.get('lieuNaissance', personne.lieuNaissance)
            
            # HARMONISATION : Utilise les noms envoyés par ton frontend
            personne.emailPerso = data.get('emailPersonnel', personne.emailPerso)
            personne.telPerso = data.get('telephonePersonnel', personne.telPerso)
            
            if data.get('sexe'): 
                personne.sexe_id = data.get('sexe')
            
            if 'photoFile' in files: # Ton front envoie photoFile
                personne.photos = files['photoFile']

            personne.save()

            # --- 7. Fin et Retour ---
            # On recharge pour renvoyer la donnée propre
            return Response({"status": "success", "message": "Mise à jour réussie"}, status=status.HTTP_200_OK)

        except Personnelles.DoesNotExist:
            return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Erreur critique: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk):
        try:
            personne = Personnelles.objects.get(pk=pk)
            serializer = PersonnelUpdateSerializer(
                personne,
                data=request.data,
                partial=True,
                context={'request': request}  # ✅ AJOUTER CECI
            )
            
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Mise à jour partielle réussie"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Personnelles.DoesNotExist:
            return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Erreur critique: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
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