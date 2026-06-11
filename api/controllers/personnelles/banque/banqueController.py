from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Banques
from api.services.personnelles.banque.banqueService import BanqueService
from api.dto.personnelles.banque.banqueDto import BanqueDto

<<<<<<< HEAD

=======
>>>>>>> 23088e43 (mon enregistrement local)
class BanqueController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                data = BanqueService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Banque trouvé avec succès",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
<<<<<<< HEAD

=======
>>>>>>> 23088e43 (mon enregistrement local)
            except Banques.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Banque non trouvé pour l'id = {id}",
                }

<<<<<<< HEAD
                return Response(
                    response,
                    status=status.HTTP_404_NOT_FOUND
                )

        else:
            data = BanqueService.getAllDto().data

=======
                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = BanqueService.getAllDto().data
>>>>>>> 23088e43 (mon enregistrement local)
            response = {
                "status": "success",
                "message": "Liste banques success",
                "data": data
            }
<<<<<<< HEAD

            return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        valiny = BanqueDto(data=request.data)

        if not valiny.is_valid():
            errors_list = []

=======
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        valiny = BanqueDto(data=request.data)
        if not valiny.is_valid():
            errors_list = []
>>>>>>> 23088e43 (mon enregistrement local)
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    errors_list.append(f"{field}: {error}")

            errors_str = "; ".join(errors_list)

            response = {
                "status": "error",
                "message": errors_str,
                "errors": valiny.errors
            }
<<<<<<< HEAD

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )

        banque = BanqueService.create(
            valiny.validated_data["nom"],
            valiny.validated_data["rib"]
        )

=======
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        banque = BanqueService.create(valiny.validated_data["nom"])
>>>>>>> 23088e43 (mon enregistrement local)
        response = {
            "status": "success",
            "message": "Banque créée avec succès",
            "data": BanqueService.getByIdDto(banque.id).data
        }
<<<<<<< HEAD

        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        valiny = BanqueDto(data=request.data)

        if not valiny.is_valid():
            errors_list = []

=======
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = BanqueDto(data=request.data)
        if not valiny.is_valid():
            errors_list = []
>>>>>>> 23088e43 (mon enregistrement local)
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    errors_list.append(f"{field}: {error}")

            errors_str = "; ".join(errors_list)

            response = {
                "status": "error",
                "message": errors_str,
                "errors": valiny.errors
            }
<<<<<<< HEAD

            return Response(
                response,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            banque = BanqueService.update(
                id,
                valiny.validated_data["nom"],
                valiny.validated_data["rib"]
            )

=======
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            banque = BanqueService.update(id, valiny.validated_data["nom"])
>>>>>>> 23088e43 (mon enregistrement local)
            response = {
                "status": "success",
                "message": "Banque mise à jour avec succès",
                "data": BanqueService.getByIdDto(banque.id).data
            }
<<<<<<< HEAD

            return Response(response, status=status.HTTP_200_OK)

=======
            return Response(response, status=status.HTTP_200_OK)
>>>>>>> 23088e43 (mon enregistrement local)
        except Banques.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Banque non trouvé pour l'id = {id}",
            }
<<<<<<< HEAD

            return Response(
                response,
                status=status.HTTP_404_NOT_FOUND
            )
=======
            return Response(response, status=status.HTTP_404_NOT_FOUND)
>>>>>>> 23088e43 (mon enregistrement local)
