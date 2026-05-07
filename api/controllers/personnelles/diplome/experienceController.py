from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.personnelles.diplome.experienceService import ExperienceService
from api.dto import ExperienceDTO

class ExperienceController(APIView):

    def get(self, request, id=None):
        try:
            if id:
                experience = ExperienceService.getById(id)
                return Response(ExperienceDTO(experience).data, status=status.HTTP_200_OK)
            
            experiences = ExperienceService.getAll()
            return Response(ExperienceDTO(experiences, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            experience = ExperienceService.create(request.data)
            return Response({
                "message": "Création réussie !",
                "data": ExperienceDTO(experience).data
            }, status=status.HTTP_201_CREATED)
        except KeyError as e:
            return Response({"error": f"Champ manquant : {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            experience = ExperienceService.update(id, request.data)
            return Response({
                "message": "Mise à jour réussie",
                "data": ExperienceDTO(experience).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            ExperienceService.delete(id)
            return Response({"message": "Supprimé avec succès"}, status=status.HTTP_200_OK) 
            # Note: Normalement on utilise 204 (No Content), mais 200 avec un message est plus pratique pour débuter sur Postman.
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)