from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.conge.ConfigPlanningService import ConfigPlanningService
from api.dto.conge.ConfigPlanningDTO import ConfigPlanningDTO

class ConfigPlanningController(APIView):
    def get(self, request):
        """Récupère si le bouton est masqué ou affiché chez le client."""
        config = ConfigPlanningService.get_or_create_config()
        dto = ConfigPlanningDTO(config)
        return Response(dto.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Met à jour le statut du switch (Bouton Masqué/Affiché)."""
        dto = ConfigPlanningDTO(data=request.data)
        if dto.is_valid():
            updated_config = ConfigPlanningService.update_status(
                active_status=dto.validated_data['active']
            )
            return Response(ConfigPlanningDTO(updated_config).data, status=status.HTTP_200_OK)
        
        return Response(dto.errors, status=status.HTTP_400_BAD_REQUEST)