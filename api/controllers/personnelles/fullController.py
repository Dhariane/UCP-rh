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

from api.models import EtatCivil,Sexes,Relations,Postes,Personnelles

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
                    "emailPerso":data.get('emailPerso'),
                    "telPerso":data.get("telPerso"),
                    "photoResidence":data.get("photoResidence"),
                    "sexe": sexe,      
                    "propos": propos,  
                    "cin": cin         
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
                
                superieur = None
                if data.get("superieur"):
                    superieur = SuperieurService.create({
                        "nom": data.get("superieur")
                    })

                # ----- Fonction -----
                fonction = FonctionService.create({
                    "nom": data.get("fonction"),
                    "dateDebut": data.get("dateDebut"),
                    "dateFin": data.get("dateFin"),
                    "financement":data.get("financement"),
                    "personnelle": personnelles,
                    "superieur": superieur,
                    "poste": poste,
                    "service": service,
                    
                })
                for exp in data.get("experiences", []):
                    ExperienceService.create({
                        "nombreExperience":exp.get("nbrExp"),
                        "entreprise": exp.get("entreprise"),
                        "poste": exp.get("posteExp"),
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
                        "poste": hist.get("posteHis"),
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
                        "prenomConjoint": fam.get("prenomConjoint"),
                        "nombreEnfant": fam.get("nombreEnfantper"),
                        "personnelle": personnelles
                    })
                
                return Response({"status": "success"}, status=201)

        except Exception as e:
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
                'contactUrgence__relation'
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
                    ]
                }
                result.append(personnelle_data)
            
            return Response(result, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)

