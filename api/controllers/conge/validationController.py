
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.conge.conge import Conge
from api.models.auth.login.loginModel import Login
from api.services.conge.validationService import ValidationService
from api.dto.conge.congeDto import CongeDTO


class ValidationController(APIView):
    """
    POST /api/conge/<id>/valider/
    Body : { "login_id": 2, "decision": "approuve" | "refuse", "motif": "..." }
    """

    def post(self, request, id):
        login_id = request.data.get('login_id')
        decision = request.data.get('decision')
        motif    = request.data.get('motif', None)

        # ── Validation des champs requis ──────────────────────────────────
        if not login_id:
            return Response({
                "status": "error",
                "message": "Le champ 'login_id' est requis."
            }, status=status.HTTP_400_BAD_REQUEST)

        if decision not in ('approuve', 'refuse'):
            return Response({
                "status": "error",
                "message": "Le champ 'decision' doit être 'approuve' ou 'refuse'."
            }, status=status.HTTP_400_BAD_REQUEST)

        if decision == 'refuse' and not motif:
            return Response({
                "status": "error",
                "message": "Le champ 'motif' est obligatoire en cas de refus."
            }, status=status.HTTP_400_BAD_REQUEST)

        # ── Appel du service ──────────────────────────────────────────────
        try:
            conge = ValidationService.valider(
                conge_id=id,
                login_id=login_id,
                decision=decision,
                motif=motif,
            )
            return Response({
                "status": "success",
                "message": f"Congé {decision} avec succès.",
                "data": CongeDTO(conge).data
            }, status=status.HTTP_200_OK)

        except Conge.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Congé introuvable (ID: {id})."
            }, status=status.HTTP_404_NOT_FOUND)

        except Login.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Login introuvable (ID: {login_id})."
            }, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Erreur inattendue : {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CongeValidationHistoriqueController(APIView):
    """
    GET /api/conge/<id>/validations/
    Retourne l'historique des validations d'un congé.
    """

    def get(self, request, id):
        try:
            conge = Conge.objects.get(pk=id)
        except Conge.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Congé introuvable (ID: {id})."
            }, status=status.HTTP_404_NOT_FOUND)

        validations = conge.validationconge_set.select_related(
            'valideur'
        ).order_by('created_at')

        data = [
            {
                "id":        v.id,
                "etape":     v.etape,
                "decision":  v.decision,
                "motif":     v.motif,
                "valideur":  str(v.valideur),
                "date":      v.created_at.strftime('%d/%m/%Y %H:%M'),
            }
            for v in validations
        ]

        return Response({
            "status": "success",
            "data": data,
            "etape_actuelle": conge.etape_validation,
        }, status=status.HTTP_200_OK)
