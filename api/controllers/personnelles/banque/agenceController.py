from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Agences
from api.services.personnelles.banque.agencesService import AgenceService 
from api.dto.personnelles.banque.agencesDto import AgenceDto
class AgenceController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                data = AgenceService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste agences success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Agences.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Agence non trouvé pour l'id = {id}",
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = AgenceService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste agences success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)   
        
    def post(self, request):
        valiny = AgenceDto(data=request.data)
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

        agence = AgenceService.create(valiny.validated_data["nom"])
        response = {
            "status": "success",
            "message": "Agence créée avec succès",
            "data": AgenceService.getByIdDto(agence.id).data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = AgenceDto(data=request.data)
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
            agence = AgenceService.update(id, valiny.validated_data["nom"])
            response = {
                "status": "success",
                "message": "Agence mise à jour avec succès",
                "data": AgenceService.getByIdDto(agence.id).data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Agences.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Agence non trouvé pour l'id = {id}",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
    
    