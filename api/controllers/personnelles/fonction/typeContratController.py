from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.fonction.typeContrat import TypeContrats
from api.services.personnelles.fonction.typeContrantService import TypeContratService
from api.dto.personnelles.fonction.typecontratDto import TypeContratDto


class TypeContratController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                data = TypeContratService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "TypeContrat récupéré avec succès",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except TypeContrats.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": f"TypeContrat non trouvé pour l'id = {id}"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            data = TypeContratService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste des types de contrat récupérée",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        valiny = TypeContratDto(data=request.data)
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

        tc = TypeContratService.create(valiny.validated_data)
        response = {
            "status": "success",
            "message": "Insertion réussie avec succès",
            "data": TypeContratDto(tc).data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        valiny = TypeContratDto(data=request.data)
        if not valiny.is_valid():
            return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            tc = TypeContratService.update(id, valiny.validated_data["TypeContrat"])
            return Response(TypeContratDto(tc).data, status=status.HTTP_200_OK)
        except TypeContrats.DoesNotExist:
            response = {
                "status": "error",
                "message": f"TypeContrat non trouvé pour l'id = {id}" 
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
