from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.personnelles.diplome.diplomeService import DiplomeService
from api.dto import DiplomeDTO

class DiplomeController(APIView):

    def get(self, request, id=None):
        try:
            if id:
                diplome = DiplomeService.getById(id)
                return Response(DiplomeDTO(diplome).data, status=status.HTTP_200_OK)
            
            diplomes = DiplomeService.getAll()
            return Response(DiplomeDTO(diplomes, many=True).data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Diplôme introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            # Important : request.data gère le JSON et le form-data (pour l'image)
            diplome = DiplomeService.create(request.data)
            return Response({
                "status": "success",
                "message": "Diplôme créé avec succès",
                "data": DiplomeDTO(diplome).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            diplome = DiplomeService.update(id, request.data)
            return Response({
                "status": "success",
                "message": "Mise à jour réussie",
                "data": DiplomeDTO(diplome).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            DiplomeService.delete(id)
            return Response({"message": "Diplôme supprimé avec succès"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Impossible de supprimer ce diplôme"}, status=status.HTTP_400_BAD_REQUEST)
