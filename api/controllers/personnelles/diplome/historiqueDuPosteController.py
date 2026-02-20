from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.personnelles.diplome.historiqueDuPosteService import HistoriqueDuPosteService
from api.dto.personnelles.diplome.historiqueDuPosteDto import HistoriqueDuPosteDTO 

class HistoriqueDuPosteController(APIView):

    def get(self, request, id=None):
        try:
            if id:
                historique = HistoriqueDuPosteService.getById(id)
                return Response(HistoriqueDuPosteDTO(historique).data, status=status.HTTP_200_OK)
            
            historiques = HistoriqueDuPosteService.getAll()
            return Response(HistoriqueDuPosteDTO(historiques, many=True).data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Historique introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            historique = HistoriqueDuPosteService.create(request.data)
            return Response({
                "message": "Historique ajouté avec succès",
                "data": HistoriqueDuPosteDTO(historique).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            historique = HistoriqueDuPosteService.update(id, request.data)
            return Response({
                "message": "Historique mis à jour",
                "data": HistoriqueDuPosteDTO(historique).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            HistoriqueDuPosteService.delete(id)
            return Response({"message": "Historique supprimé"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Erreur lors de la suppression"}, status=status.HTTP_400_BAD_REQUEST)