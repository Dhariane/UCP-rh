from rest_framework.views import    APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.fonction.fonctions import Fonctions
from api.services.personnelles.fonction.fonctionService import FonctionService
from api.dto.personnelles.fonction.fonctionDto import FonctionDto

class FonctionController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                data = FonctionService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Fonction retrieved successfully",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Fonctions.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Fonction not found for id = {id}"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            data = FonctionService.getAllDto().data
            response = {
                "status": "success",
                "message": "List of Fonctions retrieved successfully",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        valiny = FonctionDto(data=request.data)
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
        
        fonction = FonctionService.create(
            dateDebut=valiny.validated_data['dateDebut'],
            dateFin=valiny.validated_data['dateFin'],
            personnelle=valiny.validated_data['personnelle'],
            service=valiny.validated_data['service'],
            poste=valiny.validated_data['poste']
        )
        response = {
            "status": "success",
            "message": "Fonction created successfully",
            "data": FonctionDto(fonction).data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = FonctionDto(data=request.data)
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
            fonction = FonctionService.update(
                id=id,
                dateDebut=valiny.validated_data['dateDebut'],
                dateFin=valiny.validated_data['dateFin'],
                personnelle=valiny.validated_data['personnelle'],
                service=valiny.validated_data['service'],
                poste=valiny.validated_data['poste']
            )
            response = {
                "status": "success",
                "message": "Fonction updated successfully",
                "data": FonctionDto(fonction).data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Fonctions.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Fonction not found for id = {id}"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
