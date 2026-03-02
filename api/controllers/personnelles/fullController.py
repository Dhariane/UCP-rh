from api.models.fonction.typeContrat import TypeContrats
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import json
from api.dto import PersonnellesDTO
from api.services.personnelles.propos import (
    CinsService, PersonnelleServices, EtatCivilService,
    PhotosService, ProposService,SexeService,EnfantService,FamilleService)
from api.services.personnelles.fonction import FonctionService, PosteService, ServiceService, SuperieurService
from api.services.personnelles.fonction.contratService import ContratService
from api.services.personnelles.fonction.typeContrantService import TypeContratService
from api.services.personnelles.contact import ContactUrgencesService, RelationService
from api.services.personnelles.banque import CoordonneesBancaireServices, AgenceService, BanqueService
from api.services.personnelles.diplome.diplomeService import DiplomeService
from api.services.personnelles.diplome.experienceService import ExperienceService
from api.services.personnelles.diplome.formationService import FormationService
from api.services.personnelles.diplome.historiqueDuPosteService import HistoriqueDuPosteService
from api.services.personnelles.fonction.contratService import ContratService
from api.services.personnelles.fonction.typeContrantService import TypeContratService

from api.models import EtatCivil,Sexes,Relations,Postes,Personnelles,Services

class PersonnelFullController(APIView):
    renderer_classes = [JSONRenderer]
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        data = request.data
        files = request.FILES #
        try:
            experiences = json.loads(data.get("experiences", "[]"))
            diplomes = json.loads(data.get("diplomes", "[]"))
            formations = json.loads(data.get("formations", "[]"))
            enfants = json.loads(data.get("enfants", "[]"))
            historiques = json.loads(data.get("historiqueDuPoste", "[]"))
        except Exception as e:
            return Response({"error": "Format JSON invalide"}, status=400)
        # Debug pour voir ce qui arrive réellement
        print("DATA REÇUE :", data)

        try:
            with transaction.atomic():
                # 1. Récupération des objets liés (vérification existence)
                sexe_id = data.get("sexe")
                etat_civil_id = data.get("etatCivil")
                poste_id = data.get("poste")

                if not sexe_id or not etat_civil_id or not poste_id:
                    return Response({"error": "Sexe, Etat Civil et Poste sont obligatoires"}, status=400)

                # 1. Récupération des objets liés
                sexe = Sexes.objects.get(id=sexe_id)
                etatcivil = EtatCivil.objects.get(id=etat_civil_id)
                poste = Postes.objects.get(id=poste_id)
                # Récupération ou création du type de contrat
                type_contrat_id = data.get("typeContrat")  # Id ou nom envoyé depuis Postman
                if type_contrat_id:
                    try:
                        type_contrat = TypeContratService.get(type_contrat_id)
                    except TypeContrats.DoesNotExist:
                        return Response({"error": "Type de contrat invalide"}, status=400)
                else:
                    return Response({"error": "Type de contrat requis"}, status=400)
                
                service_id = data.get("service")
                service = Services.objects.get(id=service_id)

                # 2. Banque et Agence
                banque = BanqueService.create({"nom": data.get("banque")})
                agence = AgenceService.create({
                    "nom": data.get("agence"),
                    "ville": data.get("villeAgence")
                })

                # 3. Coordonnées bancaires
                image_rib = request.FILES.get('photoRib')
                print(f"DEBUG RIB: Fichier reçu = {image_rib}") # <--- Ajoute ça pour être sûr !

                coord = CoordonneesBancaireServices.create({
                    "rib": data.get("rib"),
                    "banque": banque,
                    "agence": agence,
                    "photo_rib": image_rib # On envoie le fichier au service
                })

                # 4. CIN
                cin = CinsService.create({
                    "numeroCin": data.get("cin"),
                    "dateCin": data.get("dateDelivranceCin"),
                    "lieuCin": data.get("lieuDelivranceCin")
                })

                # 5. Propos
                propos = ProposService.create({
                    "nif": data.get("nif"),
                    "stat": data.get("stat"),
                    "numeroCnaps": data.get("cnaps"),
                    "tel": data.get("contactPersonnel"),
                    "email": data.get("emailProfessionnel"),
                    "nombreEnfant": data.get("nombreEnfants") or 0,
                    "etatCivil": etatcivil
                })

                # 6. Personnelles
                # --- Dans ton Controller Django ---
                image_residence = request.FILES.get('photoResidence') 
                file_casier = request.FILES.get('casierjudiciaire') 
                acte_de_naissance = request.FILES.get('acteNaissance')  
                file_cin = request.FILES.get("cinphoto")             
                personnelles = PersonnelleServices.create({
                    "nom": data.get("nom"),
                    "prenom": data.get("prenoms"),
                    "dateNaissance": data.get("dateNaissance"),
                    "lieuNaissance": data.get("lieuNaissance"),
                    "adresse": data.get("adresse"),
                    "emailPerso": data.get('emailPersonnel'),
                    "telPerso": data.get("contactPersonnel"),
                    "sexe": sexe,
                    "propos": propos,
                    "cin": cin,
                    "photoResidence": image_residence,
                    "casierjudiciaire": file_casier,
                    "acteNaissance":acte_de_naissance,
                    "cinphoto": file_cin
                })
                # Récupération du fichier envoyé (photo du contrat)
                photo_contrat = request.FILES.get("photoContrat")

                # Création du Contrat
                contrat = ContratService.create({
                    "NumeroContrat": data.get("NumeroContrat"),
                    "photoContrat": photo_contrat,
                    "typeContrat": type_contrat,  # l'objet TypeContrat
                    "personnelle": personnelles  # l'objet Personnelles créé
                })
                # 7. Contacts d'urgence (Traitement individuel car le JSON est plat)
                # Contact 1
                if data.get("personne1"):
                    rel1 = Relations.objects.get(id=data.get("relation1"))
                    ContactUrgencesService.create({
                # Ajout de la photo principale si présente
                        "nom": data.get("personne1"),
                        "telephone": data.get("telephone1"),
                        "adresse": data.get("adresse1"),
                        "personnelle": personnelles,
                        "relation": rel1
                    })
                #photos
                photo_file = request.FILES.get('photo')
            print(f"--- DEBUG AVANT SERVICE ---")
            print(f"Fichier trouvé : {photo_file}")
            print(f"Taille du fichier : {photo_file.size if photo_file else '0'} octets")

            if photo_file:
                # On force l'appel avec des clés explicites
                PhotosService.create({
                    "nom": data.get("nom") + "_photo",
                    "data": photo_file,  # On passe l'objet InMemoryUploadedFile
                    "personnelle": personnelles.id
                })
                
                # Contact 2
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
                service = ServiceService.create({"nom": data.get("service")})
                superieur = None
                if data.get("superieur"):
                    superieur = SuperieurService.create({"nom": data.get("superieur")})

                FonctionService.create({
                    "nom": data.get("fonction"),
                    "dateDebut": data.get("dateEmbauche"),
                    "dateFin": data.get("dateSortie") if data.get("dateSortie") else None,
                    "financement":data.get("financement"),
                    "personnelle": personnelles,
                    "superieur": superieur,
                    "poste": poste,
                    "service": service,
                })

                # 9. Famille (Données à plat dans le view)
                if data.get("nomPere") or data.get("nomMere"):
                    FamilleService.create({
                        "nomPere": data.get("nomPere"),
                        "prenomPere": data.get("prenomPere"),
                        "nomMere": data.get("nomMere"),
                        "prenomMere": data.get("prenomMere"),
                        "nomConjoint": data.get("nomConjoint"),
                        "prenomConjoint": data.get("prenomConjoint"),
                        "nombreEnfant": data.get("nombreEnfants") or 0,
                        "acteMariage": request.FILES.get("acteMariage"),
                        "personnelle": personnelles
                    })

                # ----- Expériences -----
                
                for exp in experiences:
                    ExperienceService.create({
                        "nombreExperience": exp.get("nbrExp"),
                        "entreprise": exp.get("entreprise"),
                        "poste": exp.get("posteExp"),
                        "datedebut": exp.get("datedebut"),
                        "datefin": exp.get("datefin"),
                        "description": exp.get("description"),
                        "personnelle": personnelles.id
                    })

                # 3. ----- Diplômes -----
                # On utilise la liste 'diplomes' qu'on vient de parser
                for dip in diplomes:
                    DiplomeService.create({
                        "nom": dip.get("Diplome"),
                        "etablissement": dip.get("etablissement"),
                        "dateObtention": dip.get("dateObtention"),
                        "photo": request.FILES.get("photo"), # Le fichier est bien là d'après tes logs
                        "personnelle": personnelles.id
                    })

                # 4. ----- Formations -----
                
                for form in formations:
                    FormationService.create({
                        "titre": form.get("titre"),
                        "organisme": form.get("organisme"),
                        "lieu": form.get("lieu"),
                        "annee": form.get("annee"),
                        "attestation": request.FILES.get("attestation"),
                        "personnelle": personnelles.id
                    })
                
                # ----- Enfants -----
                for enf in enfants:
                    EnfantService.create({
                        "nom": enf.get("nom"),
                        "prenom": enf.get("prenom"),
                        "dateNaissance": enf.get("dateNaissance"),
                        "lieuNaissance": enf.get("lieuNaissance"),
                        "certificatVie": request.FILES.get("certificatVie"),
                        "personnelle": personnelles.id
                    })

                # ----- Historique du poste -----
                for hist in historiques:
                    HistoriqueDuPosteService.create({
                        "poste": hist.get("poste"),
                        "dateDebut": hist.get("datedebut") or hist.get("dateDebut"),
                        "dateFin": hist.get("datefin") or hist.get("dateFin"),
                        "description": hist.get("description"),
                        "personnelle": personnelles.id
                    })

                return Response({"status": "success"}, status=201)

        except Exception as e:
            print("ERREUR SERVEUR :", str(e))
            print("Champs texte reçus :", data.keys())
            print("Fichiers reçus :", request.FILES.keys())
            return Response({"error": str(e)}, status=400)

    def get(self, request):
        
        try:
            # Récupère toutes les personnelles
            personnelles_list = Personnelles.objects.all().prefetch_related(
                'sexe',
                'photos',
                'Diplome',
                'Experience',
                'Famille',
                'Enfant',
                'fonctions__service',
                'fonctions__poste',
                'fonctions__superieur',
                'propos__etatCivil',
                'cin',
                'contactUrgence__relation',
            
            )
            
            result = []
            for personnelle in personnelles_list:
                # Récupère la fonction actuelle (la plus récente)
                fonction = personnelle.fonctions.filter(
                    dateFin__isnull=True
                ).first() or personnelle.fonctions.first()
                
                # Récupère le contact urgence
                contact = personnelle.contactUrgence.first() if personnelle.contactUrgence.exists() else None
                
                # Construit l'objet de réponse
                personnelle_data = {
                    "id": personnelle.id,
                    "nom": personnelle.nom,
                    "prenom": personnelle.prenom,
                    "dateNaissance": personnelle.dateNaissance,
                    "lieuNaissance": personnelle.lieuNaissance,
                    "adresse": personnelle.adresse,
                    "emailPerso": personnelle.emailPerso,
                    "telPerso": personnelle.telPerso,
                    "photoResidence": str(personnelle.photoResidence) if personnelle.photoResidence else None,
                    
                    # Sexe
                    "sexe": {
                        "id": personnelle.sexe.id,
                        "nom": personnelle.sexe.nom
                    } if personnelle.sexe else None,
                    
                    # CIN
                    "cin": {
                        "id": personnelle.cin.id,
                        "numeroCin": personnelle.cin.numeroCin,
                        "dateCin": personnelle.cin.dateCin,
                        "lieuCin": personnelle.cin.lieuCin
                    } if personnelle.cin else None,
                    
                    # Propos
                    "propos": {
                        "id": personnelle.propos.id,
                        "nif": personnelle.propos.nif,
                        "stat": personnelle.propos.stat,
                        "numeroCnaps": personnelle.propos.numeroCnaps,
                        "tel": personnelle.propos.tel,
                        "email": personnelle.propos.email,
                        "nombreEnfant": personnelle.propos.nombreEnfant,
                        "etatCivil": {
                            "id": personnelle.propos.etatCivil.id,
                            "nom": personnelle.propos.etatCivil.nom
                        } if personnelle.propos.etatCivil else None
                    } if personnelle.propos else None,
                    
                    # Fonction complète
                    "fonction": {
                        "id": fonction.id,
                        "nom": fonction.nom,
                        "dateDebut": fonction.dateDebut,
                        "dateFin": fonction.dateFin,
                        "financement": fonction.financement,
                        "service": {
                            "id": fonction.service.id,
                            "nom": fonction.service.nom
                        } if fonction.service else None,
                        "poste": {
                            "id": fonction.poste.id,
                            "nom": fonction.poste.nom
                        } if fonction.poste else None,
                        "superieur": {
                            "id": fonction.superieur.id,
                            "nom": fonction.superieur.nom
                        } if fonction.superieur and fonction.superieur.id else None
                    } if fonction else None,
                    
                    
                    # Contact Urgence
                    "contactUrgence": {
                        "id": contact.id,
                        "nom": contact.nom,
                        "telephone": contact.telephone,
                        "adresse": contact.adresse,
                        "relation": {
                            "id": contact.relation.id,
                            "nom": contact.relation.nom
                        }
                    } if contact else None,
                    
                    # Diplômes
                    "diplomes": [
                        {
                            "id": dip.id,
                            "nom": dip.nom,
                            "etablissement": dip.etablissement,
                            "dateObtention": dip.dateObtention,
                            "photo": str(dip.photo) if dip.photo else None
                        }
                        for dip in personnelle.Diplome.all()
                    ],
                    
                    # Expériences
                    "experiences": [
                        {
                            "id": exp.id,
                            "nombreExperience":exp.nombreExperience,
                            "entreprise": exp.entreprise,
                            "poste": exp.poste,
                            "datedebut": exp.datedebut,
                            "datefin": exp.datefin,
                            "description": exp.description
                        }
                        for exp in personnelle.Experience.all()
                    ],
                    
                    # Photos
                    "photos": [
                        {
                            "id": photo.id,
                            "nom": photo.nom,
                            "data": str(photo.data) if photo.data else None
                        }
                        for photo in personnelle.photos.all()
                    ],
                    
                    # Famille
                    "famille": [
                        {
                            "id": fam.id,
                            "nomPere": fam.nomPere,
                            "prenomPere": fam.prenomPere,
                            "nomMere": fam.nomMere,
                            "prenomMere": fam.prenomMere,
                            "nomConjoint": fam.nomConjoint,
                            "prenomConjoint": fam.prenomConjoint,
                            "nombreEnfant": fam.nombreEnfant
                        }
                        for fam in personnelle.Famille.all()
                    ],
                    
                    # Enfants
                    "enfants": [
                        {
                            "id": enf.id,
                            "nom": enf.nom,
                            "prenom": enf.prenom,
                            "dateNaissance": enf.dateNaissance,
                            "lieuNaissance": enf.lieuNaissance
                        }
                        for enf in personnelle.Enfant.all()
                    ],
                    
                    # Contrats
                    "contrats": [
                        {
                            "id": c.id,
                            "NumeroContrat": c.NumeroContrat,
                            "photoContrat": str(c.photoContrat) if c.photoContrat else None,
                            "typeContrat": c.typeContrat.TypeContrat if c.typeContrat else None
                        }
                        for c in personnelle.contrat.all()
                    ]
                }
                result.append(personnelle_data)
            
            return Response(result, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)

