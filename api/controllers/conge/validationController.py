from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.conge.validationService import ValidationService
from api.models.conge.conge import Conge

class ValidationCongeController(APIView):

    def post(self, request, conge_id):
        """Valider ou refuser une étape du congé"""
        try:
            login_id = request.data.get('login_id')
            decision = request.data.get('decision')  # 'approuve' ou 'refuse'
            motif    = request.data.get('motif', None)

            # Vérifications basiques
            if not login_id:
                return Response({
                    "status": "error",
                    "message": "login_id est obligatoire"
                }, status=status.HTTP_400_BAD_REQUEST)

            if decision not in ['approuve', 'refuse']:
                return Response({
                    "status": "error",
                    "message": "decision doit être 'approuve' ou 'refuse'"
                }, status=status.HTTP_400_BAD_REQUEST)

            if decision == 'refuse' and not motif:
                return Response({
                    "status": "error",
                    "message": "motif est obligatoire en cas de refus"
                }, status=status.HTTP_400_BAD_REQUEST)

            conge = ValidationService.valider(
                conge_id = conge_id,
                login_id = login_id,
                decision = decision,
                motif    = motif,
            )

            return Response({
                "status":  "success",
                "message": "Validation enregistrée",
                "data": {
                    "conge_id": conge.id,
                    "statut":   conge.statut.statut,
                }
            }, status=status.HTTP_200_OK)

        except Conge.DoesNotExist:
            return Response({
                "status":  "error",
                "message": f"Congé introuvable (ID: {conge_id})"
            }, status=status.HTTP_404_NOT_FOUND)

        except ValueError as e:
            return Response({
                "status":  "error",
                "message": str(e)
            }, status=status.HTTP_403_FORBIDDEN)

        except Exception as e:
            return Response({
                "status":  "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, conge_id):
        """Voir l'historique des validations d'un congé"""
        try:
            conge       = Conge.objects.get(id=conge_id)
            validations = conge.validations.all()

            data = [
                {
                    "etape":    v.etape,
                    "decision": v.decision,
                    "valideur": f"{v.valideur.personnelle.prenom} {v.valideur.personnelle.nom}" if v.valideur and v.valideur.personnelle else "—",
                    "motif":    v.motif,
                    "date":     v.date,
                }
                for v in validations
            ]

            return Response({
                "status": "success",
                "data":   data
            }, status=status.HTTP_200_OK)

        except Conge.DoesNotExist:
            return Response({
                "status":  "error",
                "message": f"Congé introuvable (ID: {conge_id})"
            }, status=status.HTTP_404_NOT_FOUND)
        
    