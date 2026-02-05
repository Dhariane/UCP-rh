# api/views/propos_controller.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Propos
from api.services.personnelles.propos.proposService import ProposService
from api.dto.personnelles.propos.proposDto import ProposDTO


class ProposController(APIView):
    """
    Controller pour gérer les EtatCivil
    """

    def get(self, request, id=None):
        if id:
            try:
                data = ProposService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste demandes success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Propos.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Propos non trouvé pour l'id = {id}",
                    # "error": f"Propos non \trouvé pour l'id = {id}"
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = ProposService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste demandes success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        valiny = ProposDTO(data=request.data)
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


        propos = ProposService.create(valiny.validated_data)
        response = {
                "status": "success",
                "message": "Insertion reussis avec succes",
                "data": ProposDTO(propos).data
            }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        valiny = ProposDTO(data=request.data)
        if not valiny.is_valid():
            return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            propos = ProposService.update(id, valiny.validated_data)
            return Response(ProposDTO(propos).data, status=status.HTTP_200_OK)
        except Propos.DoesNotExist:
            response ={
                "status":"error",
                "message": f"Propos non trouvé pour l'id ={id}",
                # "error": f"Propos non trouvé pour l'id = {id}"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
