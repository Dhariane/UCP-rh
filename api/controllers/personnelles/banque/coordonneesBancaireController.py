from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import CoordonneesBancaires
from api.services.personnelles.banque.coordonneesBancaireServices import CoordonneesBancaireServices
from api.dto.personnelles.banque.coordonneBancaireDto import CoordonneesBancairesDto

class CoordonneesBancaireController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                data = CoordonneesBancaireServices.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste coordonnées bancaires success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except CoordonneesBancaires.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Coordonnée bancaire non trouvé pour l'id = {id}",
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = CoordonneesBancaireServices.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste coordonnées bancaires success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)

    
    def post(self, request):
        serializer = CoordonneesBancairesDto(data=request.data)

        if serializer.is_valid():
            coordonnee = serializer.save()

            return Response({
                "status": "success",
                "message": "Coordonnées bancaires créées avec succès",
                "data": CoordonneesBancairesDto(coordonnee).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id):
        valiny = CoordonneesBancairesDto(data=request.data)
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
            coordonnees_bancaire = CoordonneesBancaireServices.update(
                id,
                valiny.validated_data["banque"],
                valiny.validated_data["agence"],
                valiny.validated_data["rib"],
            )
            response = {
                "status": "success",
                "message": "Coordonnée bancaire mise à jour avec succès",
                "data": CoordonneesBancaireServices.getByIdDto(coordonnees_bancaire.id).data
            }
            return Response(response, status=status.HTTP_200_OK)
        except CoordonneesBancaires.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Coordonnée bancaire non trouvé pour l'id = {id}",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)