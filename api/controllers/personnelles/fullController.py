from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.renderers import JSONRenderer
from rest_framework import status

from api.dto import PersonnellesDTO
from api.services.personnelles.propos import (
    CinsService, PersonnelleServices, EtatCivilService,
    PhotosService, ProposService,SexeService,EnfantService,FamilleService)
from api.services.personnelles.fonction import FonctionService, PosteService, ServiceService, SuperieurService
from api.services.personnelles.contact import ContactUrgencesService, RelationService
from api.services.personnelles.banque import CoordonneesBancaireServices, AgenceService, BanqueService
from api.services.personnelles.diplome.diplomeService import DiplomeService
from api.services.personnelles.diplome.experienceService import ExperienceService
from api.services.personnelles.diplome.formationService import FormationService
from api.services.personnelles.diplome.historiqueDuPosteService import HistoriqueDuPosteService

from api.models import EtatCivil,Sexes,Relations,Postes
class PersonnelFullController(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = request.data
        print("DATA POSTMAN :", data)

        try:
            with transaction.atomic():
                # ----- ForeignKeys existantes -----
                sexe = Sexes.objects.get(id=data.get("sexe"))
                etatcivil = EtatCivil.objects.get(id=data.get("etatCivil"))
                relation = Relations.objects.get(id=data.get("relation"))
                poste = Postes.objects.get(id=data.get("poste"))

                # ----- Créer Agence -----
                agence_nom = data.get("agence")
                if not agence_nom:
                    return Response({"error": "Clé 'agence' manquante dans le JSON"}, status=400)

                agence = AgenceService.create({
                    "nom": agence_nom
                })
                banque = BanqueService.create({
                    "nom": data.get("banque")
                })

                # ----- Coordonnées bancaires -----
                coord = CoordonneesBancaireServices.create({
                    "rib": data.get("rib"),
                    "banque": banque,
                    "agence": agence,
                    "photoRib":data.get("photoRib")
                })

                # ----- CIN -----
                cin = CinsService.create({
                    "numeroCin": data.get("numeroCin"),
                    "dateCin": data.get("dateCin"),
                    "lieuCin": data.get("lieuCin")
                })

                # ----- Propos -----
                propos = ProposService.create({
                    "nif": data.get("nif"),
                    "stat": data.get("stat"),
                    "numeroCnaps": data.get("numeroCnaps"),
                    "tel": data.get("tel"),
                    "email": data.get("email"),
                    "nombreEnfant": data.get("nombreEnfant"),
                    "etatCivil": etatcivil
                })

                # ----- Personnelles -----
                personnelles = PersonnelleServices.create({
                    "nom": data.get("nom"),
                    "prenom": data.get("prenom"),
                    "dateNaissance": data.get("dateNaissance"),
                    "lieuNaissance": data.get("lieuNaissance"),
                    "adresse":data.get("adressePerso"),
                    "photoResidence":data.get("photoResidence"),
                    "sexe": sexe,      # ID de l'objet Sexes
                    "propos": propos,  # ID de l'objet Propos
                    "cin": cin         # ID de l'objet Cins
                })
                

                # ----- Photo -----
                photo = PhotosService.create({
                    
                    "nom": data.get("nomFichierReal"),
                    "data": data.get("photoNom"),
                    "personnelle": personnelles.id
                    
                })
                # Dans ton traitement du POST


                # ----- Contact d'urgence -----
                contactU = ContactUrgencesService.create({
                    "nom": data.get("contactNom"),
                    "telephone": data.get("telephone"),
                    "adresse": data.get("adresse"),
                    "personnelle": personnelles,
                    "relation": relation
                })

                service = ServiceService.create({
                    "nom": data.get("service")
                })
                superieur = SuperieurService.create({
                    "nom": data.get("superieur")
                })

                # ----- Fonction -----
                fonction = FonctionService.create({
                    "nom": data.get("fonction"),
                    "dateDebut": data.get("dateDebut"),
                    "dateFin": data.get("dateFin"),
                    "personnelle": personnelles,
                    "superieur": superieur,
                    "poste": poste,
                    "service": service
                })
                for exp in data.get("experiences", []):
                    ExperienceService.create({
                        "entreprise": exp.get("entreprise"),
                        "poste": exp.get("poste"),
                        "datedebut": exp.get("datedebut"),
                        "datefin": exp.get("datefin"),
                        "description": exp.get("description"),
                        "personnelle": personnelles.id
                    })

                # Diplômes
                for dip in data.get("diplomes", []):
                    DiplomeService.create({
                        "nom": dip.get("Diplome"),
                        "etablissement": dip.get("etablissement"),
                        "dateObtention": dip.get("dateObtention"),
                        "photo": dip.get("photo"),
                        "personnelle": personnelles.id
                    })

                # Formations
                for form in data.get("formations", []):
                    FormationService.create({
                        "titre": form.get("titreFormation"),
                        "organisme": form.get("organisme"),
                        "datedebut": form.get("datedebutFor"),
                        "datefin": form.get("datefinFor"),
                        "attestation": form.get("attestation"),
                        "personnelle": personnelles.id
                    })

                # Historique du Poste
                for hist in data.get("historiques", []):
                    HistoriqueDuPosteService.create({
                        "poste": hist.get("poste"),
                        "société": hist.get("société"),
                        "datedebut": hist.get("datedebutHis"),
                        "datefin": hist.get("datefinHis"),
                        "description": hist.get("description"),
                        "personnelle": personnelles.id
                    })

                # Enfants
                for enf in data.get("enfants", []):
                    EnfantService.create({
                        "nom": enf.get("nomEnfant"),
                        "prenom": enf.get("prenomEnfant"),
                        "dateNaissance": enf.get("dateNaissanceEnfant"),
                        "lieuNaissance": enf.get("lieuNaissanceEnfant"),
                        "personnelle": personnelles.id
                    })
                for fam in data.get("familles", []):
                    FamilleService.create({
                        "nomPere": fam.get("nomPere"),
                        "prenomPere": fam.get("prenomPere"),
                        "nomMere": fam.get("nomMere"),
                        "prenomMere": fam.get("prenomMere"),
                        "nomConjoint": fam.get("nomConjoint"),
                        "nombreEnfant": fam.get("nombreEnfantper"),
                        "prenomConjoint": fam.get("prenomConjoint"),
                        "personnelle": personnelles
                    })
                
                return Response({"status": "success"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)

    # def get(self, request, id=None):
    #     if id:
    #         try:
    #             # Récupérer les informations du personnel
    #             personnelle = Personnelles.objects.get(id=id)

    #             # Récupérer les informations associées au personnel
    #             propos = Propos.objects.get(personnelle=personnelle)
    #             cin = Cins.objects.get(personnelle=personnelle)
    #             photo = Photos.objects.get(personnelle=personnelle)
    #             contact_urgence = ContactUrgences.objects.get(personnelle=personnelle)
    #             fonction = Fonctions.objects.get(personnelle=personnelle)
    #             poste = Postes.objects.get(fonction=fonction)
    #             service = Services.objects.get(fonction=fonction)
    #             superieur = Superieur.objects.get(fonction=fonction)
    #             coord_bancaire = CoordonneesBancaires.objects.get(personnelle=personnelle)
    #             agence = Agences.objects.get(coordonneesbancaire=coord_bancaire)
    #             banque = Banques.objects.get(coordonneesbancaire=coord_bancaire)
    #             sexe = Sexes.objects.get(personnelle=personnelle)
    #             etatcivil = EtatCivil.objects.get(propos=propos)
    #             relation = Relations.objects.get(contacturgences=contact_urgence)

    #             # Construire la réponse JSON
    #             response_data = self._build_personnelle_response(
    #                 personnelle, propos, cin, photo, contact_urgence, fonction,
    #                 poste, service, superieur, coord_bancaire, agence, banque,
    #                 sexe, etatcivil, relation
    #             )

    #             return Response(response_data, status=status.HTTP_200_OK)

    #         except Personnelles.DoesNotExist:
    #             return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)
    #         except Exception as e:
    #             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    #     else:
    #         # Récupérer tous les personnels
    #         personnels = Personnelles.objects.all()
    #         serializer = PersonnellesDTO(personnels, many=True)
    #         response = {
    #             "status": "success",
    #             "message": "Liste des personnels récupérée",
    #             "data": serializer.data
    #         }
    #         return Response(response, status=status.HTTP_200_OK)

    # def _build_personnelle_response(self, personnelle, propos, cin, photo, contact_urgence, fonction,
    #                                poste, service, superieur, coord_bancaire, agence, banque,
    #                                sexe, etatcivil, relation):
    #     return {
    #         "personnelle": {
    #             "id": personnelle.id,
    #             "nom": personnelle.nom,
    #             "prenom": personnelle.prenom,
    #             "dateNaissance": personnelle.dateNaissance,
    #             "lieuNaissance": personnelle.lieuNaissance,
    #             "sexe": {
    #                 "id": sexe.id,
    #                 "nom": sexe.nom
    #             },
    #             "propos": {
    #                 "id": propos.id,
    #                 "nifStat": propos.nifStat,
    #                 "numeroCnaps": propos.numeroCnaps,
    #                 "tel": propos.tel,
    #                 "email": propos.email,
    #                 "nombreEnfant": propos.nombreEnfant,
    #                 "etatCivil": {
    #                     "id": etatcivil.id,
    #                     "nom": etatcivil.nom
    #                 }
    #             },
    #             "cin": {
    #                 "id": cin.id,
    #                 "numeroCin": cin.numeroCin,
    #                 "dateCin": cin.dateCin,
    #                 "lieuCin": cin.lieuCin
    #             },
    #             "photo": {
    #                 "id": photo.id,
    #                 "nom": photo.nom,
    #                 "data": photo.data
    #             },
    #             "contact_urgence": {
    #                 "id": contact_urgence.id,
    #                 "nom": contact_urgence.nom,
    #                 "telephone": contact_urgence.telephone,
    #                 "adresse": contact_urgence.adresse,
    #                 "relation": {
    #                     "id": relation.id,
    #                     "nom": relation.nom
    #                 }
    #             },
    #             "fonction": {
    #                 "id": fonction.id,
    #                 "dateDebut": fonction.dateDebut,
    #                 "dateFin": fonction.dateFin,
    #                 "poste": {
    #                     "id": poste.id,
    #                     "nom": poste.nom,
    #                     "grade": poste.grade
    #                 },
    #                 "service": {
    #                     "id": service.id,
    #                     "nom": service.nom
    #                 },
    #                 "superieur": {
    #                     "id": superieur.id,
    #                     "nom": superieur.nom
    #                 }
    #             },
    #             "coordonnees_bancaires": {
    #                 "id": coord_bancaire.id,
    #                 "rib": coord_bancaire.rib,
    #                 "banque": {
    #                     "id": banque.id,
    #                     "nom": banque.nom
    #                 },
    #                 "agence": {
    #                     "id": agence.id,
    #                     "nom": agence.nom
    #                 }
    #             }
    #         }
    #     }