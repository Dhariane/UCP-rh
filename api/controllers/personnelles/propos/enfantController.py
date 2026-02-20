from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.personnelles.propos.enfantService import EnfantService
from api.dto.personnelles.propos.enfantDto import EnfantDTO

class EnfantController(APIView):

    def get(self, request, id=None):
        try:
            if id:
                enfant = EnfantService.getById(id)
                return Response(EnfantDTO(enfant).data, status=status.HTTP_200_OK)
            
            enfants = EnfantService.getAll()
            return Response(EnfantDTO(enfants, many=True).data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Enfant introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            enfant = EnfantService.create(request.data)
            return Response({
                "message": "Enfant enregistré avec succès",
                "data": EnfantDTO(enfant).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            enfant = EnfantService.update(id, request.data)
            return Response({
                "message": "Informations de l'enfant mises à jour",
                "data": EnfantDTO(enfant).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            EnfantService.delete(id)
            return Response({"message": "Fiche enfant supprimée"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Erreur lors de la suppression"}, status=status.HTTP_400_BAD_REQUEST)