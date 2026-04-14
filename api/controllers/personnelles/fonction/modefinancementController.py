from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.fonction.modefinancement import ModeFinancement
from api.services.personnelles.fonction.modefinancementService import ModeFinancementService
from api.dto.personnelles.fonction.modefinancementDto import ModefinancementDto

class ModeFinancementController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                data = ModeFinancementService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Mode de financement récupéré avec succès",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except ModeFinancement.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Mode de financement introuvable pour l'id = {id}"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            data = ModeFinancementService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste des modes de financement récupérée avec succès",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        valiny = ModefinancementDto(data=request.data)
        if not valiny.is_valid():
            errors_list = []
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    errors_list.append(f"{field}: {error}")

            errors_str = "; ".join(errors_list)

            response = {
                "status": "error",
                "message": errors_str,
                "errors": valiny.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        mode = ModeFinancementService.create(valiny.validated_data)
        
        response = {
            "status": "success",
            "message": "Mode de financement créé avec succès",
            "data": ModefinancementDto(mode).data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = ModefinancementDto(data=request.data)
        if not valiny.is_valid():
            errors_list = []
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    errors_list.append(f"{field}: {error}")

            errors_str = "; ".join(errors_list)

            response = {
                "status": "error",
                "message": errors_str,
                "errors": valiny.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            mode = ModeFinancementService.update(
                id=id,
                nom=valiny.validated_data['nom']
            )
            response = {
                "status": "success",
                "message": "Mode de financement mis à jour avec succès",
                "data": ModefinancementDto(mode).data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ModeFinancement.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Mode de financement introuvable pour l'id = {id}"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    # AJOUTER CETTE MÉTHODE DELETE
    def delete(self, request, id):
        try:
            ModeFinancementService.delete(id)
            response = {
                "status": "success",
                "message": "Mode de financement supprimé avec succès"
            }
            return Response(response, status=status.HTTP_200_OK)
        except ModeFinancement.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Mode de financement introuvable pour l'id = {id}"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)