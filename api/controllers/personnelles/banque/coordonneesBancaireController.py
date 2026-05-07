from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from api.models.banque.coordonneesBancaires import CoordonneesBancaires
from api.services.personnelles.banque.coordonneesBancaireServices import CoordonneesBancaireServices
from api.dto.personnelles.banque.coordonneBancaireDto import CoordonneesBancairesDto

class CoordonneesBancaireController(APIView):
    # Crucial pour la réception de la photo du RIB
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id=None):
        if id:
            try:
                coordonnee = CoordonneesBancaireServices.getById(id)
                return Response({
                    "status": "success",
                    "data": CoordonneesBancairesDto(coordonnee).data
                }, status=status.HTTP_200_OK)
            except CoordonneesBancaires.DoesNotExist:
                return Response({
                    "status": "error", 
                    "message": "Coordonnée bancaire introuvable"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            queryset = CoordonneesBancaireServices.getAll()
            return Response({
                "status": "success",
                "data": CoordonneesBancairesDto(queryset, many=True).data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CoordonneesBancairesDto(data=request.data)
        if serializer.is_valid():
            # On utilise les données validées du serializer pour le service
            coordonnee = CoordonneesBancaireServices.create(serializer.validated_data)
            return Response({
                "status": "success",
                "message": "RIB ajouté avec succès",
                "data": CoordonneesBancairesDto(coordonnee).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            # partial=True permet de modifier uniquement la photo ou uniquement le RIB
            serializer = CoordonneesBancairesDto(data=request.data, partial=True)
            if serializer.is_valid():
                coordonnee = CoordonneesBancaireServices.update(id, serializer.validated_data)
                return Response({
                    "status": "success",
                    "message": "Mise à jour réussie",
                    "data": CoordonneesBancairesDto(coordonnee).data
                }, status=status.HTTP_200_OK)
            
            return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        except CoordonneesBancaires.DoesNotExist:
            return Response({"status": "error", "message": "Non trouvé"}, status=status.HTTP_404_NOT_FOUND)