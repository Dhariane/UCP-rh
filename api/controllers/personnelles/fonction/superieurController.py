import errno
from nt import error
from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Superieur
from api.services.personnelles.fonction.superieurService import SuperieurService
from api.dto.personnelles.fonction.superieurDto import SuperieurDto

class SuperieurController(APIView):
    def get(self,request,id=None):
        if id:
            try:
                data=SuperieurService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste demandes success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Superieur.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Service non trouvé pour l'id = {id}",
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            data = SuperieurService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste demandes success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
    def post(self, request):
        valiny = SuperieurDto(data=request.data)
        if not valiny.is_valid():
            error_list = []
            for field, field_error in valiny.errors.items():
                for error in field_error:
                    error_list.append(f"{field}: {error}")
            errors_str = "; ".join(error_list)
            response = {
                "status": "error",
                "message": errors_str,
                "errors": valiny.errors
            }
            
        etat = SuperieurService.create(valiny.validated_data["nom"])    
        response = {
            "status": "success",
            "message": "Insertion reussis avec succes",
            "data": SuperieurDto(etat).data     
        }
        return Response(response, status=status.HTTP_201_CREATED)
                
        