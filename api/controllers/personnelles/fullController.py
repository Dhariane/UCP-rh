from argparse import Action

from api.models.banque.banques import Banques
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
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json
from api.dto import PersonnellesDTO
from api.dto.fullpersonnelDto import PersonnelFullSerializer
from api.dto.fullUpdatePersonnelDto import PersonnelUpdateSerializer
from api.models.propos.enfant import Enfant
from api.models.propos.propos import Propos
from api.models.fonction.fonctions import Fonctions as FonctionsModel
from api.services.personnelles.propos import (
    CinsService, PersonnelleServices, EtatCivilService,
    PhotosService, ProposService, SexeService, EnfantService, FamilleService)
from api.services.personnelles.fonction import FonctionService, PosteService, ServiceService
from api.services.personnelles.fonction.contratService import ContratService
from api.services.personnelles.fonction.typeContrantService import TypeContratService
from api.services.personnelles.contact import ContactUrgencesService, RelationService
from api.services.personnelles.banque import CoordonneesBancaireServices, AgenceService, BanqueService
from api.services.personnelles.diplome.diplomeService import DiplomeService
from api.services.personnelles.diplome.experienceService import ExperienceService
from api.services.personnelles.diplome.formationService import FormationService
from api.services.personnelles.fonction.modefinancementService import ModeFinancementService
from api.models import EtatCivil, Sexes, Relations, Postes, Personnelles, Services, ModeFinancement, Cins, fonction
from api.services.auth.login.loginService import LoginService
from django.db.models import Prefetch
from rest_framework.permissions import AllowAny


class PersonnelFullController(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    permission_classes = [AllowAny]

    # ══════════════════════════════════════════════════════
    # GET — un seul get qui gère archive / détail / liste
    # ══════════════════════════════════════════════════════
    def get(self, request, pk=None):
        import traceback
        from django.db.models import Prefetch
        from api.models.fonction.contrat import Contrat
        try:
            # CAS 1 : ARCHIVE
            if pk and request.query_params.get('archive') == 'true':
                from api.dto.contratHistoryDto import ContratHistorySerializer
                historique = Contrat.history.filter(personnelle_id=pk).order_by('-history_date')
                serializer = ContratHistorySerializer(historique, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # CAS 2 : DÉTAIL
            elif pk:
                personne = Personnelles.objects.prefetch_related(
                    'sexe', 'cins', 'propos_list', 'propos_list__etatCivil',
                    'diplomes', 'Experience', 'Enfant', 'contactUrgence', 'photos',
                    Prefetch(
                        'contrats',
                        queryset=Contrat.objects.select_related('fonction', 'typeContrat', 'service', 'financement')
                    )
                ).get(pk=pk)
                serializer = PersonnelFullSerializer(personne, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

            # CAS 3 : LISTE
            else:
                personnes = Personnelles.objects.all().prefetch_related(
                    'sexe', 'cins', 'photos',
                    Prefetch(
                        'contrats',
                        queryset=Contrat.objects.select_related('fonction', 'typeContrat', 'service', 'financement')
                    )
                )
                serializer = PersonnelFullSerializer(personnes, many=True, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Personnelles.DoesNotExist:
            return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            traceback.print_exc()
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # ══════════════════════════════════════════════════════
    # POST
    # ══════════════════════════════════════════════════════
    def post(self, request):
        data = request.data
        files = {k: v for k, v in request.FILES.items()}
        for f in files.values():
            f.seek(0)

        try:
            import json as json_module
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
                sexe_id       = data.get("sexe")
                etat_civil_id = data.get("etatCivil")
                poste_id      = data.get("poste")

                if not sexe_id or not etat_civil_id:
                    return Response({"error": "Sexe et Etat Civil sont obligatoires"}, status=400)

                try:
                    sexe        = Sexes.objects.get(id=sexe_id)
                    etatcivil   = EtatCivil.objects.get(id=etat_civil_id)
                    service     = Services.objects.get(id=data.get("service"))
                    financement = ModeFinancement.objects.get(id=data.get("financement"))
                except (Sexes.DoesNotExist, Services.DoesNotExist, ModeFinancement.DoesNotExist) as e:
                    return Response({"error": f"Référence introuvable : {str(e)}"}, status=400)

                poste = None
                if poste_id and poste_id not in ["", "null", "undefined"]:
                    try:
                        poste = Postes.objects.get(id=poste_id)
                    except Postes.DoesNotExist:
                        return Response({"error": "Le poste spécifié n'existe pas"}, status=400)

                type_contrat_id = data.get("typecontrat")
                if type_contrat_id:
                    try:
                        type_contrat = TypeContratService.get(type_contrat_id)
                    except Exception:
                        return Response({"error": "Type de contrat invalide"}, status=400)
                else:
                    return Response({"error": "Type de contrat requis"}, status=400)

                fonction_obj = FonctionsModel.objects.get(id=data.get("fonction"))
                banque_nom   = data.get("banque")
                banque, _    = Banques.objects.get_or_create(nom=banque_nom)
                agence       = AgenceService.create({"nom": data.get("agence"), "ville": data.get("villeAgence")})

                personnelles = PersonnelleServices.create({
                    "nom": data.get("nom"), "prenom": data.get("prenom"),
                    "dateNaissance": data.get("dateNaissance"), "lieuNaissance": data.get("lieuNaissance"),
                    "adresse": data.get("adresse"), "emailPerso": data.get('emailPersonnel'),
                    "telPerso": data.get("telephonePersonnel"), "quartier": data.get("quartier"),
                    "ville": data.get("ville"), "sexe": sexe,
                    "photoResidence": files.get('photoresidence'),
                    "casierjudiciaire": files.get('photoCasier'),
                    "acteNaissance": files.get('photoacteNaissance'),
                    "cinphoto": files.get("photoCin")
                })

                CinsService.create({
                    "numeroCin": data.get("cin"), "dateCin": data.get("dateDelivranceCin"),
                    "lieuCin": data.get("lieuDelivranceCin"), "numeroDuplicata": data.get("numeroDuplicata"),
                    "dateDuplicata": data.get("dateDuplicataCin"), "lieuDuplicata": data.get("lieuDuplicataCin"),
                    "personnelle": personnelles
                })

                propos = ProposService.create({
                    "nif": data.get("nif"), "stat": data.get("stat"),
                    "numeroCnaps": data.get("cnaps"), "tel": data.get("contactProfessionnel"),
                    "email": data.get("emailProfessionnel"),
                    "nombreEnfant": data.get("nombreEnfants") or 0,
                    "etatCivil": etatcivil, "personnelle": personnelles
                })

                CoordonneesBancaireServices.create({
                    "rib": data.get("rib"), "banque": banque, "agence": agence,
                    "photo_rib": files.get('photoRibFile'), "personnelle": personnelles.id
                })

                ContratService.create({
                    "NumeroContrat": data.get("NumeroContrat"), "periodeEssai": data.get("periodeEssai"),
                    "dateFinEssai": data.get("dateFinEssai"), "salaire": data.get("honoraire"),
                    "photoContrat": files.get("photoContrat"), "typeContrat": type_contrat,
                    "personnelle": personnelles, "fonction": fonction_obj, "service": service,
                    "dateDebut": data.get("dateEmbauche"), "dateFin": data.get("dateSortie") or None,
                    "financement": financement
                })

                if data.get("personne1"):
                    rel1 = Relations.objects.get(id=data.get("relation1"))
                    ContactUrgencesService.create({
                        "nom": data.get("personne1"), "telephone": data.get("telephone1"),
                        "adresse": data.get("adresse1"), "personnelle": personnelles, "relation": rel1
                    })

                if data.get("personne2"):
                    rel2 = Relations.objects.get(id=data.get("relation2"))
                    ContactUrgencesService.create({
                        "nom": data.get("personne2"), "telephone": data.get("telephone2"),
                        "adresse": data.get("adresse2"), "personnelle": personnelles, "relation": rel2
                    })

                photo_file = files.get('photoFile')
                if photo_file:
                    PhotosService.create({
                        "nom": data.get("nom") + "_photo", "data": photo_file,
                        "personnelle": personnelles.id
                    })

                superieurs_ids = data.get("superieurs", "[]")
                if isinstance(superieurs_ids, str):
                    superieurs_ids = json.loads(superieurs_ids)
                if superieurs_ids:
                    from api.models.auth.login.loginModel import Login
                    for login_id in superieurs_ids:
                        try:
                            login_superieur = Login.objects.get(id=login_id)
                            fonction.superieurs.add(login_superieur)
                        except Login.DoesNotExist:
                            pass

                if data.get("nomPere") or data.get("nomMere"):
                    FamilleService.create({
                        "nomPere": data.get("nomPere"), "nomMere": data.get("nomMere"),
                        "nomConjoint": data.get("nomConjoint"), "prenomConjoint": data.get("prenomConjoint"),
                        "nombreEnfant": data.get("nombreEnfants") or 0,
                        "acteMariage": files.get("acteMariage"), "telConjoint": data.get("telConjoint"),
                        "adresseConjoint": data.get("adresseConjoint"), "emailConjoint": data.get("emailConjoint"),
                        "personnelle": personnelles
                    })

                for exp in experiences:
                    ExperienceService.create({
                        "entreprise": exp.get("entreprise"), "poste": exp.get("poste"),
                        "datedebut": exp.get("dateDebut"), "datefin": exp.get("dateFin"),
                        "description": exp.get("description"), "personnelle": personnelles.id
                    })

                for i, dip in enumerate(diplomes):
                    DiplomeService.create({
                        "type_diplome": dip.get("type_diplome"), "filiere": dip.get("filiere"),
                        "lieu": dip.get("lieu"), "etablissement": dip.get("etablissement"),
                        "annneObtention": dip.get("annee"), "photo": files.get(f"diplome_file_{i}"),
                        "personnelle": personnelles.id
                    })

                for i, form in enumerate(formations):
                    FormationService.create({
                        "titre": form.get("theme"), "organisme": form.get("organisme"),
                        "lieu": form.get("lieu"), "annee": form.get("annee"),
                        "attestation": files.get(f"formation_file_{i}"), "personnelle": personnelles.id
                    })

                for i, enf in enumerate(enfants):
                    donnees_enfant = {
                        "nom": enf.get("nom"), "prenom": enf.get("prenom"),
                        "dateNaissance": enf.get("dateNaissance"), "lieuNaissance": enf.get("lieuNaissance"),
                        "personnelle": personnelles.id, "sexe": sexe.id
                    }
                    fichier = request.FILES.get(f"certificat_enfant_{i}")
                    if fichier:
                        donnees_enfant["certificatVie"] = fichier
                    EnfantService.create(donnees_enfant)

            if propos:
                try:
                    LoginService.create(propos)
                except Exception as email_error:
                    print(f"⚠️ Email échoué : {email_error}")

            return Response({
                "status": "success",
                "message": "Personnel créé avec succès. Un email a été envoyé.",
                "matricule": personnelles.matricule
            }, status=201)

        except Exception as e:
            print("ERREUR CRITIQUE :", str(e))
            return Response({"error": str(e)}, status=400)

    # ══════════════════════════════════════════════════════
    # PUT
    # ══════════════════════════════════════════════════════
    @transaction.atomic
    def put(self, request, pk):
        try:
            personne = Personnelles.objects.select_for_update().get(pk=pk)
            data  = request.data
            files = request.FILES

            from api.models.fonction.contrat import Contrat
            contrat_lie = Contrat.objects.filter(personnelle=personne).first()
            if contrat_lie:
                contrat_lie.NumeroContrat = data.get('NumeroContrat', contrat_lie.NumeroContrat)
                contrat_lie.salaire       = data.get('honoraire',     contrat_lie.salaire)
                contrat_lie.dateDebut     = data.get('dateEmbauche',  contrat_lie.dateDebut)
                contrat_lie.dateFin       = data.get('dateSortie',    contrat_lie.dateFin)
                if data.get('service'):     contrat_lie.service_id     = data.get('service')
                if data.get('typecontrat'): contrat_lie.typeContrat_id = data.get('typecontrat')
                if data.get('financement'): contrat_lie.financement_id = data.get('financement')
                if 'photoContrat' in files: contrat_lie.photoContrat   = files['photoContrat']
                contrat_lie.save()

            cin_lie  = Cins.objects.filter(personnelle=personne).first()
            cin_vals = {
                "numeroCin": data.get('num_cin_input') or data.get('cin'),
                "dateCin":   data.get('dateDelivranceCin'),
                "lieuCin":   data.get('lieuDelivranceCin')
            }
            if cin_lie:
                for key, val in cin_vals.items():
                    if val is not None: setattr(cin_lie, key, val)
                if 'photoCin' in files: cin_lie.photo = files['photoCin']
                cin_lie.save()
            else:
                Cins.objects.create(personnelle=personne, **cin_vals)

            propos_lie = Propos.objects.filter(personnelle=personne).first()
            if propos_lie:
                propos_lie.numeroCnaps  = data.get('cnaps')              or propos_lie.numeroCnaps
                propos_lie.nif          = data.get('nif')                or propos_lie.nif
                propos_lie.stat         = data.get('stat')               or propos_lie.stat
                propos_lie.tel          = data.get('telephonePersonnel') or propos_lie.tel
                propos_lie.email        = data.get('emailPersonnel')     or propos_lie.email
                propos_lie.nombreEnfant = data.get('nombreEnfants')      or propos_lie.nombreEnfant
                if data.get('etatCivil'): propos_lie.etatCivil_id = data.get('etatCivil')
                propos_lie.save()

            from api.models.banque.coordonneesBancaires import CoordonneesBancaires
            coord = CoordonneesBancaires.objects.filter(personnelle=personne).first()
            if coord:
                coord.rib = data.get('rib') or coord.rib
                if data.get('banque'): coord.banque_id = data.get('banque')
                if data.get('agence'): coord.agence_id = data.get('agence')
                if 'photoRibFile' in files: coord.photo_rib = files['photoRibFile']
                coord.save()

            from api.models.propos.famille import Famille
            famille_lie = Famille.objects.filter(personnelle=personne).first()
            if famille_lie:
                for field in ["nomPere", "prenomPere", "nomMere", "prenomMere",
                              "nomConjoint", "prenomConjoint", "telConjoint",
                              "adresseConjoint", "emailConjoint"]:
                    val = data.get(field)
                    if val is not None: setattr(famille_lie, field, val)
                famille_lie.save()

            personne.nom           = data.get('nom',                personne.nom)
            personne.prenom        = data.get('prenom',             personne.prenom)
            personne.adresse       = data.get('adresse',            personne.adresse)
            personne.dateNaissance = data.get('dateNaissance',      personne.dateNaissance)
            personne.lieuNaissance = data.get('lieuNaissance',      personne.lieuNaissance)
            personne.emailPerso    = data.get('emailPersonnel',     personne.emailPerso)
            personne.telPerso      = data.get('telephonePersonnel', personne.telPerso)
            if data.get('sexe'): personne.sexe_id = data.get('sexe')
            if 'photoFile' in files: personne.photos = files['photoFile']
            personne.save()

            return Response({"status": "success", "message": "Mise à jour réussie"}, status=status.HTTP_200_OK)

        except Personnelles.DoesNotExist:
            return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Erreur critique: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # ══════════════════════════════════════════════════════
    # PATCH
    # ══════════════════════════════════════════════════════
    def patch(self, request, pk):
        try:
            personne   = Personnelles.objects.get(pk=pk)
            serializer = PersonnelUpdateSerializer(
                personne, data=request.data, partial=True, context={'request': request}
            )
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "message": "Mise à jour partielle réussie"}, status=status.HTTP_200_OK)
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Personnelles.DoesNotExist:
            return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"Erreur critique: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # ══════════════════════════════════════════════════════
    # DELETE
    # ══════════════════════════════════════════════════════
    def delete(self, request, pk):
        try:
            personne = Personnelles.objects.get(pk=pk)
            personne.delete()
            return Response(
                {"message": f"Le personnel ID {pk} et toutes ses données liées ont été supprimés."},
                status=status.HTTP_200_OK
            )
        except Personnelles.DoesNotExist:
            return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)