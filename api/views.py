from django.shortcuts import render

# Create your views here.
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

# Importe tes modèles ici
from api.models import EtatCivil, Sexes, Relations, Postes, Personnelles

class PersonnelFullController(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        data = request.data
        print("DATA REÇUE :", data)

        try:
            with transaction.atomic():
                # 1. RÉCUPÉRATION DES OBJETS LIÉS (Foreign Keys)
                # On utilise les clés exactes envoyées par le front
                try:
                    sexe = Sexes.objects.get(id=data.get("sexe"))
                    etatcivil = EtatCivil.objects.get(id=data.get("etatCivil"))
                    # Le front envoie 'relation1', le code attendait 'relation'
                    relation_id = data.get("relation1") 
                    relation = Relations.objects.get(id=relation_id)
                    poste = Postes.objects.get(id=data.get("poste"))
                except ObjectDoesNotExist as e:
                    return Response({"error": f"Référence manquante en base : {str(e)}"}, status=400)

                # 2. CRÉATION DES SERVICES DE BASE
                agence = AgenceService.create({"nom": data.get("agence")})
                banque = BanqueService.create({"nom": data.get("banque")})

                # 3. COORDONNÉES BANCAIRES
                coord = CoordonneesBancaireServices.create({
                    "rib": data.get("rib"),
                    "banque": banque,
                    "agence": agence,
                    "photoRib": request.FILES.get("photoRib") # Pour les fichiers
                })

                # 4. CIN (Harmonisation des noms des clés)
                cin = CinsService.create({
                    "numeroCin": data.get("cin"),
                    "dateCin": data.get("dateDelivranceCin"),
                    "lieuCin": data.get("lieuDelivranceCin")
                })

                # 5. PROPOS
                propos = ProposService.create({
                    "nif": data.get("nif"),
                    "stat": data.get("stat"),
                    "numeroCnaps": data.get("cnaps"),
                    "tel": data.get("contactPersonnel"),
                    "email": data.get("emailPersonnel"),
                    "nombreEnfant": data.get("nombreEnfants") or 0,
                    "etatCivil": etatcivil
                })

                # 6. PERSONNEL (Note: 'prenoms' avec un 's' dans ton QueryDict)
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
                    "cin": cin         
                })

                # 7. CONTACT D'URGENCE (Utilise personne1 et relation1)
                ContactUrgencesService.create({
                    "nom": data.get("personne1"),
                    "telephone": data.get("telephone1"),
                    "adresse": data.get("adresse1"),
                    "personnelle": personnelles,
                    "relation": relation
                })

                # 8. SERVICE & FONCTION
                service_obj = ServiceService.create({"nom": data.get("service")})
                
                superieur = None
                if data.get("superieur"):
                    superieur = SuperieurService.create({"nom": data.get("superieur")})

                FonctionService.create({
                    "nom": data.get("fonction"),
                    "dateDebut": data.get("dateEmbauche"), # 'dateEmbauche' dans ton front
                    "dateFin": data.get("dateSortie"),
                    "financement": data.get("financement"),
                    "personnelle": personnelles,
                    "superieur": superieur,
                    "poste": poste,
                    "service": service_obj,
                })

                # 9. TRAITEMENT DES LISTES JSON (IMPORTANT : json.loads)
                # Expériences
                experiences_data = json.loads(data.get("experiences", "[]"))
                for exp in experiences_data:
                    ExperienceService.create({
                        "entreprise": exp.get("entreprise"),
                        "poste": exp.get("poste"),
                        "datedebut": exp.get("dateDebut"),
                        "datefin": exp.get("dateFin"),
                        "description": exp.get("description"),
                        "personnelle": personnelles.id
                    })

                # Enfants
                enfants_data = json.loads(data.get("enfants", "[]"))
                for enf in enfants_data:
                    EnfantService.create({
                        "nom": enf.get("nom"),
                        "prenom": enf.get("prenom"),
                        "dateNaissance": enf.get("dateNaissance"),
                        "personnelle": personnelles.id
                    })

                # Diplômes (Details textuels)
                diplomes_data = json.loads(data.get("diplomes_details", "[]"))
                for dip in diplomes_data:
                    DiplomeService.create({
                        "nom": dip.get("intitule"),
                        "etablissement": dip.get("etablissement"),
                        "dateObtention": dip.get("annee"),
                        "personnelle": personnelles.id
                    })

                # 10. FAMILLE (Données directes de la page 2)
                FamilleService.create({
                    "nomPere": data.get("nomPere"),
                    "prenomPere": data.get("prenomPere"),
                    "nomMere": data.get("nomMere"),
                    "prenomMere": data.get("prenomMere"),
                    "nomConjoint": data.get("nomConjoint"),
                    "prenomConjoint": data.get("prenomConjoint"),
                    "nombreEnfant": data.get("nombreEnfants"),
                    "personnelle": personnelles
                })

                return Response({"message": "Inscription réussie"}, status=201)

        except Exception as e:
            # On print l'erreur complète dans le terminal Django pour débugger
            import traceback
            traceback.print_exc()
            return Response({"error": str(e)}, status=400)