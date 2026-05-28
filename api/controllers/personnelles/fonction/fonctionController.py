from rest_framework.views import APIView
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
                return Response({
                    "status": "error",
                    "message": f"Fonction not found for id = {id}"
                }, status=status.HTTP_404_NOT_FOUND)
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
        # On ne traite plus que le champ "nom"
        valiny = FonctionDto(data=request.data)
        if not valiny.is_valid():
            return Response({"status": "error", "errors": valiny.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # Le service doit maintenant être simplifié pour ne créer qu'un "nom"
        fonction = FonctionService.create(valiny.validated_data)
        
        return Response({
            "status": "success",
            "message": "Fonction created successfully",
            "data": FonctionDto(fonction).data
        }, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = FonctionDto(data=request.data, partial=True)
        if not valiny.is_valid():
            return Response({"status": "error", "errors": valiny.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # On met à jour uniquement le champ "nom"
            fonction = FonctionService.update(id, **valiny.validated_data)
            return Response({
                "status": "success",
                "message": "Fonction updated successfully",
                "data": FonctionDto(fonction).data
            }, status=status.HTTP_200_OK)
        except Fonctions.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Fonction not found for id = {id}"
            }, status=status.HTTP_404_NOT_FOUND)
