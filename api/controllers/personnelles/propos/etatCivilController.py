# api/views/propos_controller.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import EtatCivil
from api.services.personnelles.propos.etatCivilService import EtatCivilService
from api.dto.personnelles.propos.etatCivilDto import EtatCivilDTO


class EtatCivilController(APIView):
    """
    Controller pour gérer les EtatCivil
    """

    def get(self, request, id=None):
        if id:
            try:
                data = EtatCivilService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste demandes success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except EtatCivil.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"EtatCivil non trouvé pour l'id = {id}",
                    # "error": f"EtatCivil non \trouvé pour l'id = {id}"
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = EtatCivilService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste demandes success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        valiny = EtatCivilDTO(data=request.data)
        if not valiny.is_valid():
            # Transformer les erreurs en une seule string séparée par "; "
            errors_list = []
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    errors_list.append(f"{field}: {error}")

            errors_str = "; ".join(errors_list)  # Une seule string

            response = {
                "status": "error",
                "message": errors_str,  # toutes les erreurs dans "message"
                "errors": valiny.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


        etat = EtatCivilService.create(valiny.validated_data["nom"])
        response = {
                "status": "success",
                "message": "Insertion reussis avec succes",
                "data": EtatCivilDTO(etat).data
            }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        valiny = EtatCivilDTO(data=request.data)
        if not valiny.is_valid():
            return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            etat = EtatCivilService.update(id, valiny.validated_data["nom"])
            return Response(EtatCivilDTO(etat).data, status=status.HTTP_200_OK)
        except EtatCivil.DoesNotExist:
            response ={
                "status":"error",
                "message": f"EtatCivil non trouvé pour l'id ={id}",
                # "error": f"EtatCivil non trouvé pour l'id = {id}"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
