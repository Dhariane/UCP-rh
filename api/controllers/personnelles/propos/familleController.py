from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Famille
from api.services.personnelles.propos.FamilleService import FamilleService
from api.dto.personnelles.propos.familleDto import FamilleDto

class FamilleController(APIView):

    def get(self,request,id=None):
        if id:
            try:
                data = FamilleService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste de la famille success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Famille.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f" non trouvé pour l'id = {id}",
                }
                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = FamilleService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste famille success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        valiny = FamilleDto(data=request.data)
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
        
        # Utilisez les données validées (valiny.validated_data)
        familles = FamilleService.create(valiny.validated_data)
        response = {
            "status": "success",
            "message": "Famille ajouter avec succès",
            "data": valiny.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    def put(self, request, id):
        valiny = FamilleDto(data=request.data)
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
        