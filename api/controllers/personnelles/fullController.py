import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

# Modèles
from api.models import EtatCivil, Sexes, Relations, Postes, Personnelles

# Services
from api.services.personnelles.propos import (
    CinsService, PersonnelleServices, EtatCivilService,
    ProposService, SexeService, EnfantService, FamilleService, PhotosService
)
from api.services.personnelles.fonction import (
    FonctionService, PosteService, ServiceService, SuperieurService
)
from api.services.personnelles.contact import (
    ContactUrgencesService, RelationService
)
from api.services.personnelles.banque import (
    CoordonneesBancaireServices, AgenceService, BanqueService
)
from api.services.personnelles.diplome.diplomeService import DiplomeService
from api.services.personnelles.diplome.experienceService import ExperienceService
from api.services.auth.login.loginService import LoginService

class PersonnelFullController(APIView):
    renderer_classes = [JSONRenderer]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        data = request.data
        try:
            # Parsing des données JSON envoyées en FormData
            experiences = json.loads(data.get("experiences", "[]"))
            diplomes = json.loads(data.get("diplomes", "[]"))
            formations = json.loads(data.get("formations", "[]"))
            enfants = json.loads(data.get("enfants", "[]"))
            historiques = json.loads(data.get("historiqueDuPoste", "[]"))
        except Exception as e:
            return Response({"error": "Format JSON invalide"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. Vérification des objets liés obligatoires
                sexe_id = data.get("sexe")
                etat_civil_id = data.get("etatCivil")
                poste_id = data.get("poste")

                if not sexe_id or not etat_civil_id or not poste_id:
                    return Response({"error": "Sexe, Etat Civil et Poste sont obligatoires"}, status=400)

                sexe = Sexes.objects.get(id=sexe_id)
                etatcivil = EtatCivil.objects.get(id=etat_civil_id)
                poste = Postes.objects.get(id=poste_id)

                # 2. Banque et Agence
                banque = BanqueService.create({"nom": data.get("banque")})
                agence = AgenceService.create({
                    "nom": data.get("agence"),
                    "ville": data.get("villeAgence")
                })

                # 3. Coordonnées bancaires
                image_rib = request.FILES.get('photoRib')
                CoordonneesBancaireServices.create({
                    "rib": data.get("rib"),
                    "banque": banque,
                    "agence": agence,
                    "photo_rib": image_rib
                })

                # 4. CIN
                cin = CinsService.create({
                    "numeroCin": data.get("cin"),
                    "dateCin": data.get("dateDelivranceCin"),
                    "lieuCin": data.get("lieuDelivranceCin")
                })

                # 5. Propos (Contient l'email pour le login)
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
                image_residence = request.FILES.get('photoResidence') 
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
                })

                # 7. Photo de profil
                photo_file = request.FILES.get('photo')
                if photo_file:
                    PhotosService.create({
                        "nom": data.get("nom") + "_photo",
                        "data": photo_file,
                        "personnelle": personnelles.id
                    })

                # 8. Contacts d'urgence
                if data.get("personne1"):
                    rel1 = Relations.objects.get(id=data.get("relation1"))
                    ContactUrgencesService.create({
                        "nom": data.get("personne1"),
                        "telephone": data.get("telephone1"),
                        "adresse": data.get("adresse1"),
                        "personnelle": personnelles,
                        "relation": rel1
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

                # 9. Fonction
                service = ServiceService.create({"nom": data.get("service")})
                superieur = None
                if data.get("superieur"):
                    superieur = SuperieurService.create({"nom": data.get("superieur")})

                FonctionService.create({
                    "nom": data.get("fonction"),
                    "dateDebut": data.get("dateEmbauche"),
                    "dateFin": data.get("dateSortie") if data.get("dateSortie") else None,
                    "financement": data.get("financement"),
                    "personnelle": personnelles,
                    "superieur": superieur,
                    "poste": poste,
                    "service": service,
                })

                # 10. Famille et Enfants
                if data.get("nomPere") or data.get("nomMere"):
                    FamilleService.create({
                        "nomPere": data.get("nomPere"),
                        "prenomPere": data.get("prenomPere"),
                        "nomMere": data.get("nomMere"),
                        "prenomMere": data.get("prenomMere"),
                        "nomConjoint": data.get("nomConjoint"),
                        "prenomConjoint": data.get("prenomConjoint"),
                        "nombreEnfant": data.get("nombreEnfants") or 0,
                        "personnelle": personnelles
                    })

                for enf in enfants:
                    EnfantService.create({
                        "nom": enf.get("nom"),
                        "prenom": enf.get("prenom"),
                        "dateNaissance": enf.get("dateNaissance"),
                        "lieuNaissance": enf.get("lieuNaissance"),
                        "personnelle": personnelles.id
                    })

                # 11. Expériences, Diplômes, Formations
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

                for dip in diplomes:
                    DiplomeService.create({
                        "nom": dip.get("Diplome"),
                        "etablissement": dip.get("etablissement"),
                        "dateObtention": dip.get("dateObtention"),
                        "photo": request.FILES.get("photo"),
                        "personnelle": personnelles.id
                    })

                for form in formations:
                    FormationService.create({
                        "titre": form.get("titre"),
                        "organisme": form.get("organisme"),
                        "datedebut": form.get("datedebut"),
                        "datefin": form.get("datefin"),
                        "attestation": request.FILES.get("attestation"),
                        "personnelle": personnelles.id
                    })

                # --- ACTION FINALE : CRÉATION DU LOGIN ET ENVOI MAIL ---
                # On utilise l'instance 'propos' créée à l'étape 5
                LoginService.create(propos)

                return Response({"status": "success", 
                                 "message": "Personnel et accès créés avec succès Son Compte est creer et un email de notification a été envoyé"},
                                 status=201)

        except Exception as e:
            print("ERREUR SERVEUR :", str(e))
            return Response({"error": str(e)}, status=400)

    def get(self, request):
        try:
            personnelles_list = Personnelles.objects.all().prefetch_related(
                'sexe', 'photos', 'Diplome', 'Experience', 'Famille', 'Enfant',
                'fonctions__service', 'fonctions__poste', 'fonctions__superieur',
                'propos__etatCivil', 'cin', 'contactUrgence__relation'
            )
            
            result = []
            for personnelle in personnelles_list:
                fonction = personnelle.fonctions.filter(dateFin__isnull=True).first() or personnelle.fonctions.first()
                contact = personnelle.contactUrgence.first() if personnelle.contactUrgence.exists() else None
                
                personnelle_data = {
                    "id": personnelle.id,
                    "nom": personnelle.nom,
                    "prenom": personnelle.prenom,
                    "emailPerso": personnelle.emailPerso,
                    "sexe": {"id": personnelle.sexe.id, "nom": personnelle.sexe.nom} if personnelle.sexe else None,
                    "propos": {
                        "email": personnelle.propos.email if personnelle.propos else None,
                        "tel": personnelle.propos.tel if personnelle.propos else None,
                    },
                    "fonction": {
                        "nom": fonction.nom if fonction else None,
                        "poste": fonction.poste.nom if fonction and fonction.poste else None,
                        "service": fonction.service.nom if fonction and fonction.service else None,
                    }
                }
                # Tu peux ajouter ici les autres champs si nécessaire pour ta liste
                result.append(personnelle_data)
            
            return Response(result, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)