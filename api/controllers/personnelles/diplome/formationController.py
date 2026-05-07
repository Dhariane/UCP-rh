from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.personnelles.diplome.formationService import FormationService
from api.dto.personnelles.diplome.formationDto import FormationDTO

class FormationController(APIView):

    def get(self, request, id=None):
        try:
            if id:
                formation = FormationService.getById(id)
                return Response(FormationDTO(formation).data, status=status.HTTP_200_OK)
            
            formations = FormationService.getAll()
            return Response(FormationDTO(formations, many=True).data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Formation introuvable"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            formation = FormationService.create(request.data)
            return Response({
                "message": "Formation enregistrée avec succès",
                "data": FormationDTO(formation).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            formation = FormationService.update(id, request.data)
            return Response({
                "message": "Formation mise à jour",
                "data": FormationDTO(formation).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            FormationService.delete(id)
            return Response({"message": "Formation supprimée"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Erreur lors de la suppression"}, status=status.HTTP_400_BAD_REQUEST)