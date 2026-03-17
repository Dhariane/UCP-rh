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
from api.models import EtatCivil,Sexes,Relations,Postes,Personnelles,Services,ModeFinancement
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
                    "telPerso": data.get("contactPersonnel"),
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
                    "personnelle": personnelles

                })

                # 5. Propos
                propos = ProposService.create({
                    "nif": data.get("nif"),
                    "stat": data.get("stat"),
                    "numeroCnaps": data.get("cnaps"),
                    "tel": data.get("contactPersonnel"),
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
                        "prenomPere": data.get("prenomPere"),
                        "nomMere": data.get("nomMere"),
                        "prenomMere": data.get("prenomMere"),
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
                        "personnelle": personnelles.id
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
    def put(self, request, pk):
        try:
            # 1. On récupère l'instance principale
            personne = Personnelles.objects.get(pk=pk)
            data = request.data
            files = request.FILES

            # 2. Mise à jour des tables liées simples (CIN et Propos)
            if personne.cin:
                personne.cin.numeroCin = data.get('numeroCin', personne.cin.numeroCin)
                personne.cin.dateCin = data.get('dateCin', personne.cin.dateCin)
                personne.cin.lieuCin = data.get('lieuCin', personne.cin.lieuCin)
                personne.cin.save()

            if personne.propos:
                personne.propos.numeroCnaps = data.get('numeroCnaps', personne.propos.numeroCnaps)
                personne.propos.tel = data.get('tel', personne.propos.tel)
                personne.propos.email = data.get('email', personne.propos.email)
                personne.propos.nombreEnfant = data.get('nombreEnfant', personne.propos.nombreEnfant)
                if data.get('etatCivil'):
                    personne.propos.etatCivil_id = data.get('etatCivil')
                personne.propos.save()

            # 3. Mise à jour des Coordonnées Bancaires
            coord = getattr(personne, 'coordonnees_bancaires', None)
            if coord:
                coord.rib = data.get('rib', coord.rib)
                if data.get('banque'):
                    coord.banque_id = data.get('banque')
                if data.get('agence'):
                    coord.agence_id = data.get('agence')
                if files.get('photo_rib'): # Vérifie bien le nom du champ file envoyé
                    coord.photo_rib = files.get('photo_rib')
                coord.save()

            # 4. Mise à jour du Personnel (table principale)
            personne.nom = data.get('nom', personne.nom)
            personne.prenom = data.get('prenom', personne.prenom)
            personne.adresse = data.get('adresse', personne.adresse)
            personne.telPerso = data.get('telPerso', personne.telPerso)
            
            if files.get('cinphoto'): personne.cinphoto = files.get('cinphoto')
            if files.get('photoResidence'): personne.photoResidence = files.get('photoResidence')

            personne.save()

            # 5. MISE À JOUR DES LISTES (Diplômes, Enfants, Expériences)
            # On vide et on recrée uniquement si les données sont présentes dans la requête
            
            # Exemple pour Diplômes
            if 'diplomes' in data or any(key.startswith('diplomes[') for key in data):
                personne.Diplome.all().delete()
                i = 0
                while f'diplomes[{i}][nom]' in data:
                    Diplome.objects.create(
                        personnelle=personne,
                        nom=data.get(f'diplomes[{i}][nom]'),
                        etablissement=data.get(f'diplomes[{i}][etablissement]'),
                        dateObtention=data.get(f'diplomes[{i}][dateObtention]')
                    )
                    i += 1

            # Exemple pour Enfants
            if 'enfants' in data or any(key.startswith('enfants[') for key in data):
                personne.Enfant.all().delete()
                j = 0
                while f'enfants[{j}][nom]' in data:
                    Enfant.objects.create(
                        personnelle=personne,
                        nom=data.get(f'enfants[{j}][nom]'),
                        prenom=data.get(f'enfants[{j}][prenom]'),
                        dateNaissance=data.get(f'enfants[{j}][dateNaissance]'),
                        lieuNaissance=data.get(f'enfants[{j}][lieuNaissance]')
                    )
                    j += 1

            # 6. RELOAD & SERIALIZE (C'est ici qu'on corrige ton problème d'affichage)
            # On refait un GET complet en base de données pour tout charger proprement
            personne_complete = Personnelles.objects.prefetch_related(
                'sexe', 'cin', 'propos', 'coordonnees_bancaires', 
                'contrat', 'fonctions', 'Diplome', 'Experience', 'Enfant'
            ).get(pk=pk)

            serializer = PersonnelFullSerializer(personne_complete, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Personnelles.DoesNotExist:
            return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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