from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Cins
from api.services.personnelles.propos.CinsService import CinsService
from api.dto.personnelles.propos.CinsDto import CinsDTO

class CinsController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                poste = CinsService.getById(id)
                data = CinsDTO(poste).data
                response = {
                    "status": "success",
                    "message": "Liste cins success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Cins.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Cins non trouvé pour l'id = {id}",
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            cins = CinsService.getAll()
            data = CinsDTO(cins, many=True).data
            response = {
                "status": "success",
                "message": "Liste cins success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        valiny = CinsDTO(data=request.data)
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

        cins = CinsService.create(valiny.validated_data['numeroCin'],
                                  valiny.validated_data['dateCin'],
                                  valiny.validated_data['lieuCin'])
        response = {
            "status": "success",
            "message": "Cins créée avec succès",
            "data": CinsService(cins).data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = CinsDTO(data=request.data)
        if not valiny.is_valid():
            return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            etat = CinsService.update(id,
                                        valiny.validated_data['numeroCin'],
                                        valiny.validated_data['dateCin'],
                                        valiny.validated_data['lieuCin'])
            return Response(CinsService(etat).data, status=status.HTTP_200_OK)
        except Cins.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Cins non trouvé pour l'id = {id}",
            }

            return Response(response,
                status=status.HTTP_404_NOT_FOUND
            )