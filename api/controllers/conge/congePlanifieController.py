from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from datetime import date

from api.models.conge.congePlanifieModel import CongePlanifie
from api.models.conge.soldeConge import SoldeConge
from api.models.conge.typeConges import TypeConge
from api.models.propos.personnelles import Personnelles
from api.dto.conge.congePlanifieDTO import CongePlanifieDTO
from api.dto.conge.soldeCongeDto import SoldeCongeDTO


# ─────────────────────────────────────────────────────────────────────────────
# HELPER : formate les erreurs ValidationError Django → string lisible
# ─────────────────────────────────────────────────────────────────────────────
def _format_validation_error(e: ValidationError) -> str:
    if hasattr(e, 'message_dict'):
        messages = []
        for field, errors in e.message_dict.items():
            for msg in errors:
                messages.append(msg)
        return ' '.join(messages)
    if hasattr(e, 'messages'):
        return ' '.join(e.messages)
    return str(e)


# ─────────────────────────────────────────────────────────────────────────────
# 1. SWITCH PLANIFICATION (GET /api/conges-planifies/)
#    Consulté par CongeList.tsx pour afficher/masquer le bouton
#    "Modifier Congé Planifié"
# ─────────────────────────────────────────────────────────────────────────────
class ConfigPlanificationController(APIView):

    def get(self, request):
        """
        Retourne l'état du switch de planification.
        Cherche dans la table ConfigPlanningModel (ou retourne False par défaut).
        """
        try:
            from api.models.conge.configPlanning import ConfigPlanningModel
            config = ConfigPlanningModel.objects.first()
            return Response(
                {"active": config.active if config else False},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # Si le modèle n'existe pas encore, on retourne False sans crash
            return Response({"active": False}, status=status.HTTP_200_OK)


# ─────────────────────────────────────────────────────────────────────────────
# 2. LISTER & CRÉER (GET + POST /api/conges-planifies/<personnel_id>/)
# ─────────────────────────────────────────────────────────────────────────────
class CongePlanifieController(APIView):

    # ── GET : liste des congés planifiés d'un personnel ──────────────────────
    def get(self, request, personnel_id):
        try:
            conges = (
                CongePlanifie.objects
                .select_related('type_conge')
                .filter(personnel_id=personnel_id)
                .order_by('-date_debut')
            )
            serializer = CongePlanifieDTO(conges, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"Erreur de récupération : {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ── POST : créer un congé planifié ────────────────────────────────────────
    def post(self, request, personnel_id):
        try:
            # Vérification personnel
            try:
                personnel = Personnelles.objects.get(id=personnel_id)
            except Personnelles.DoesNotExist:
                return Response(
                    {"error": "Personnel non trouvé"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Extraction des champs
            data          = request.data
            type_conge_id = data.get('type_conge_id')
            date_debut    = data.get('date_debut')
            date_fin      = data.get('date_fin')
            description   = data.get('description', '')

            # Champs obligatoires
            if not all([type_conge_id, date_debut, date_fin]):
                return Response(
                    {"error": "type_conge_id, date_debut et date_fin sont requis"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Vérification type congé
            try:
                type_conge = TypeConge.objects.get(id=type_conge_id)
            except TypeConge.DoesNotExist:
                return Response(
                    {"error": "Le type de congé spécifié n'existe pas"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Création — full_clean() calcule nombre_jours + vérifie le solde
            # post_save signal → met à jour SoldeConge (utilise, total +2, reste)
            conge = CongePlanifie(
                personnel=personnel,
                type_conge=type_conge,
                date_debut=date_debut,
                date_fin=date_fin,
                description=description,
            )
            conge.save()  # appelle full_clean() en interne

            # Retourne le solde mis à jour pour que le front rafraîchisse
            # sans second appel réseau
            annee_conge = conge.date_debut.year
            solde_data  = {}
            try:
                solde = SoldeConge.objects.get(
                    personnel=personnel,
                    annee=annee_conge
                )
                solde_data = SoldeCongeDTO(solde).data
            except SoldeConge.DoesNotExist:
                pass

            return Response(
                {
                    "status":            "success",
                    "message":           "Congé planifié créé avec succès",
                    "id":                conge.id,
                    "nombre_jours":      conge.nombre_jours,
                    "solde_mis_a_jour":  solde_data,
                },
                status=status.HTTP_201_CREATED
            )

        except ValidationError as e:
            return Response(
                {"error": _format_validation_error(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ─────────────────────────────────────────────────────────────────────────────
# 3. DÉTAIL, MODIFIER & SUPPRIMER (GET + PATCH + DELETE
#    /api/conges-planifies/detail/<id>/)
# ─────────────────────────────────────────────────────────────────────────────
class CongePlanifieDetailController(APIView):

    # ── GET : un seul congé planifié ─────────────────────────────────────────
    def get(self, request, id):
        try:
            conge      = CongePlanifie.objects.select_related('type_conge').get(id=id)
            serializer = CongePlanifieDTO(conge)
            return Response(
                {"status": "success", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        except CongePlanifie.DoesNotExist:
            return Response(
                {"error": "Congé planifié non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ── PATCH : modifier un congé planifié ────────────────────────────────────
    def patch(self, request, id):
        try:
            conge = CongePlanifie.objects.get(id=id)
            data  = request.data

            # Mise à jour des champs fournis
            if 'type_conge_id' in data:
                try:
                    conge.type_conge = TypeConge.objects.get(id=data['type_conge_id'])
                except TypeConge.DoesNotExist:
                    return Response(
                        {"error": "Le type de congé spécifié n'existe pas"},
                        status=status.HTTP_404_NOT_FOUND
                    )

            if 'date_debut'  in data: conge.date_debut  = data['date_debut']
            if 'date_fin'    in data: conge.date_fin    = data['date_fin']
            if 'description' in data: conge.description = data['description']

            # full_clean() recalcule nombre_jours + vérifie le solde
            # post_save signal (created=False) → recalcule utilise sans +2 bonus
            conge.save()

            serializer = CongePlanifieDTO(conge)
            return Response(
                {
                    "status":  "success",
                    "message": "Planning modifié avec succès",
                    "data":    serializer.data,
                },
                status=status.HTTP_200_OK
            )

        except CongePlanifie.DoesNotExist:
            return Response(
                {"error": "Congé planifié non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )
        except ValidationError as e:
            return Response(
                {"error": _format_validation_error(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # ── DELETE : supprimer un congé planifié ──────────────────────────────────
    def delete(self, request, id):
        try:
            conge = CongePlanifie.objects.get(id=id)
            conge.delete()
            # post_delete signal → annule le +2 et recalcule le solde
            return Response(
                {
                    "status":  "success",
                    "message": "Le congé planifié a été supprimé avec succès",
                },
                status=status.HTTP_200_OK
            )
        except CongePlanifie.DoesNotExist:
            return Response(
                {"error": "Congé planifié non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ─────────────────────────────────────────────────────────────────────────────
# 4. SOLDE ACTUEL (GET /api/solde_conge/<personnel_id>/)
#    Appelé par fetchSolde() dans AdminCongesPlanifiesModal
# ─────────────────────────────────────────────────────────────────────────────
class SoldeCongeController(APIView):

    def get(self, request, personnel_id):
        try:
            annee_courante = date.today().year
            solde = SoldeConge.objects.get(
                personnel_id=personnel_id,
                annee=annee_courante
            )
            serializer = SoldeCongeDTO(solde)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except SoldeConge.DoesNotExist:
            return Response(
                {
                    "error": f"Aucun solde initialisé pour l'année {date.today().year}"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )