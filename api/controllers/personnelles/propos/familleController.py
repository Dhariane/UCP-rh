from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Famille
from api.services.personnelles.propos.FamilleService import FamilleService
from api.dto.personnelles.propos.familleDto import FamilleDto

class FamilleController(APIView):

    def get(self, request, id): # Ajoute =None ici
        if id:
            try:
                # Utilise l'ID pour récupérer le DTO
                data = FamilleService.getByIdDto(id).data
                return Response({"status": "success", "data": data}, status=200)
            except Famille.DoesNotExist:
                return Response({"status": "error", "message": "Non trouvé"}, status=404)
        else:
            data = FamilleService.getAllDto().data
            return Response({"status": "success", "data": data}, status=200)
    def post(self, request):
        valiny = FamilleDto(data=request.data)
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
        
        # Utilisez les données validées (valiny.validated_data)
        familles = FamilleService.create(valiny.validated_data)
        response = {
            "status": "success",
            "message": "Famille ajouter avec succès",
            "data": valiny.data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    def put(self, request, id):
        # On passe partial=True pour autoriser le PATCH
        serializer = FamilleDto(data=request.data, partial=True)
        if serializer.is_valid():
            # On envoie tout le dictionnaire validé au service
            instance = FamilleService.update(id, serializer.validated_data)
            return Response({"status": "success", "data": FamilleDto(instance).data})
        return Response(serializer.errors, status=400)

    def patch(self, request, id):
        return self.put(request, id)
        