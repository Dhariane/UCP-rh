from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from api.services.personnelles.propos import (
    CinsService, PersonnelleServices, EtatCivilService,
    ProposService, SexeService, EnfantService, FamilleService
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

from api.models import EtatCivil, Sexes, Relations, Postes


class PersonnelFullController(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = request.data

        try:
            with transaction.atomic():

                # ========================
                # FK
                # ========================
                sexe = Sexes.objects.get(id=data.get("sexe"))
                etatcivil = EtatCivil.objects.get(id=data.get("etatCivil"))
                poste = Postes.objects.get(id=data.get("poste"))

                # ========================
                # CIN
                # ========================
                cin = CinsService.create({
                    "numeroCin": data.get("cin"),
                    "dateCin": data.get("dateDelivranceCin"),
                    "lieuCin": data.get("lieuDelivranceCin")
                })

                # ========================
                # PROPOS
                # ========================
                propos = ProposService.create({
                    "nif": data.get("nif"),
                    "stat": data.get("stat"),
                    "numeroCnaps": data.get("cnaps"),
                    "tel": data.get("contactPersonnel"),
                    "email": data.get("emailProfessionnel"),
                    "nombreEnfant": data.get("nombreEnfants"),
                    "etatCivil": etatcivil
                })

                # ========================
                # PERSONNELLE
                # ========================
                personnelle = PersonnelleServices.create({
                    "nom": data.get("nom"),
                    "prenom": data.get("prenoms"),
                    "dateNaissance": data.get("dateNaissance"),
                    "lieuNaissance": data.get("lieuNaissance"),
                    "adresse": data.get("adresse"),
                    "emailPerso": data.get("emailPersonnel"),
                    "telPerso": data.get("contactPersonnel"),
                    "sexe": sexe,
                    "propos": propos,
                    "cin": cin
                })

                # ========================
                # BANQUE
                # ========================
                agence = AgenceService.create({
                    "nom": data.get("agence"),
                    "ville": data.get("villeAgence")
                })

                banque = BanqueService.create({
                    "nom": data.get("banque")
                })

                CoordonneesBancaireServices.create({
                    "rib": data.get("rib"),
                    "banque": banque,
                    "agence": agence,
                    "personnelle": personnelle
                })

                # ========================
                # SERVICE / SUPERIEUR
                # ========================
                service = ServiceService.create({
                    "nom": data.get("service")
                })

                superieur = None
                if data.get("superieur"):
                    superieur = SuperieurService.create({
                        "nom": data.get("superieur")
                    })

                # ========================
                # FONCTION
                # ========================
                FonctionService.create({
                    "nom": data.get("fonction"),
                    "dateDebut": data.get("dateEmbauche"),
                    "dateFin": data.get("dateSortie"),
                    "personnelle": personnelle,
                    "poste": poste,
                    "service": service,
                    "superieur": superieur
                })

                # ========================
                # CONTACTS URGENCE
                # ========================

                if data.get("personne1"):
                    relation1 = Relations.objects.get(id=data.get("relation1"))
                    ContactUrgencesService.create({
                        "nom": data.get("personne1"),
                        "telephone": data.get("telephone1"),
                        "adresse": data.get("adresse1"),
                        "personnelle": personnelle,
                        "relation": relation1
                    })

                if data.get("personne2"):
                    relation2 = Relations.objects.get(id=data.get("relation2"))
                    ContactUrgencesService.create({
                        "nom": data.get("personne2"),
                        "telephone": data.get("telephone2"),
                        "adresse": data.get("adresse2"),
                        "personnelle": personnelle,
                        "relation": relation2
                    })

                # ========================
                # ENFANTS
                # ========================
                for enf in data.get("enfants", []):
                    EnfantService.create({
                        "nom": enf.get("nom"),
                        "prenom": enf.get("prenom"),
                        "dateNaissance": enf.get("dateNaissance"),
                        "personnelle": personnelle
                    })

                # ========================
                # EXPERIENCES
                # ========================
                for exp in data.get("experiences", []):
                    ExperienceService.create({
                        "entreprise": exp.get("entreprise"),
                        "poste": exp.get("poste"),
                        "datedebut": exp.get("dateDebut"),
                        "datefin": exp.get("dateFin"),
                        "description": exp.get("description"),
                        "personnelle": personnelle
                    })

                # ========================
                # DIPLOMES
                # ========================
                for dip in data.get("diplomes_details", []):
                    DiplomeService.create({
                        "nom": dip.get("intitule"),
                        "etablissement": dip.get("etablissement"),
                        "annee": dip.get("annee"),
                        "personnelle": personnelle
                    })

                # ========================
                # FAMILLE
                # ========================
                FamilleService.create({
                    "nomPere": data.get("nomPere"),
                    "prenomPere": data.get("prenomPere"),
                    "nomMere": data.get("nomMere"),
                    "prenomMere": data.get("prenomMere"),
                    "nomConjoint": data.get("nomConjoint"),
                    "prenomConjoint": data.get("prenomConjoint"),
                    "personnelle": personnelle
                })

                return Response({"status": "success"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)