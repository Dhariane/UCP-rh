from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Personnelles
from api.services.personnelles.propos.personnellesService import PersonnellesService
from api.dto.personnelles.propos.personnellesDto import PersonnellesDTO

class PersonnelleController(APIView):

    def get(self, requst,id=None):
        if id:
            try:
                data = PersonnellesService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste personnelles success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Personnelles.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Personnelle non trouvé pour l'id = {id}",
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = PersonnellesService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste personnelles success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        valiny = PersonnellesDTO(data=request.data)
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
        

        personnelle = PersonnellesService.create(valiny)
        response = {
            "status": "success",
            "message": "Personnelle créée avec succès",
            "data": valiny.data
            # "data": PersonnellesService.getByIdDto(personnelle.id).data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = PersonnellesDTO(data=request.data)
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
        