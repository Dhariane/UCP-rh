from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from api.models.conge.conge import Conge
from api.services.conge.congeService import CongeServices   # Ajuste le chemin selon ton architecture
from api.dto.conge.congeDto import CongeDTO                # Ajuste le chemin


class CongeController(APIView):
    # Parser pour supporter JSON + éventuels fichiers (si tu ajoutes des justificatifs plus tard)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, id=None):
        if id:
            try:
                conge = CongeServices.getById(id)
                serializer = CongeDTO(conge)
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except Conge.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": f"Demande de congé non trouvée (ID: {id})"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            # Liste toutes les demandes
            conges = CongeServices.getAll()
            serializer = CongeDTO(conges, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        """Créer une nouvelle demande de congé"""
        serializer = CongeDTO(data=request.data)

        if serializer.is_valid():
            try:
                conge = CongeServices.create(serializer.validated_data)
                
                return Response({
                    "status": "success",
                    "message": "Demande de congé créée avec succès",
                    "data": CongeDTO(conge).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """Mettre à jour une demande de congé"""
        try:
            serializer = CongeDTO(data=request.data, partial=True)
            
            if serializer.is_valid():
                conge = CongeServices.update(id, serializer.validated_data)
                return Response({
                    "status": "success",
                    "message": "Demande mise à jour avec succès",
                    "data": CongeDTO(conge).data
                }, status=status.HTTP_200_OK)
            
            return Response({
                "status": "error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Conge.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Demande de congé non trouvée"
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        """Support explicite de la méthode PATCH"""
        return self.put(request, id)
    
    def delete(self, request, id):
        try:
            CongeServices.delete(id)
            return Response({
                    "status": "success",
                    "message": "Demande supprimée avec succès",
            },status=status.HTTP_204_NO_CONTENT)
        except Conge.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Demande de congé non trouvée (ID: {id})"
            }, status=status.HTTP_404_NOT_FOUND)