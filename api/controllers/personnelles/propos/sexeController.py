from urllib import response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Sexes
from api.services.personnelles.propos.sexeService import SexeService
from api.dto.personnelles.propos.sexeDto import SexeDTO

class SexeController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                data=SexeService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste demandes success",
                    "data": data
                }
                return  Response(response, status=status.HTTP_200_OK)
            except Sexe.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Sexe non trouvé pour l'id = {id}",
                    # "error": f"Sexe non trouvé pour l'id = {id}"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            data= SexeService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste demandes success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
    def post(self, request):
        valiny = SexeDTO(data=request.data)
        if not valiny.is_valid():
            error_list = []
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    error_list.append(f"{field}: {error}")
            errors_str = "; ".join(error_list)

            response = {
                "status": "error",
                "message": errors_str,
                "errors": valiny.errors
            }


        etat = SexeService.create(valiny.validated_data["nom"])
        response = {
                "status": "success",
                "message": "Insertion reussis avec succes",
                "data": SexeDTO(etat).data     
            }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, id):
            valiny=SexeDTO(data=request.data)
            if not valiny.is_valid():
                return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)
                
            try:
                sexe = SexeService.update(id, valiny.validated_data["nom"])
                return Response(SexeDTO(sexe).data, status=status.HTTP_200_OK)
            except Sexe.DoesNotExist:
                response ={
                    "status": "error",
                    "message": f"Sexe non trouvé pour l'id = {id}",
                    # "error": f"Sexe non trouvé pour l'id = {id}"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
                
