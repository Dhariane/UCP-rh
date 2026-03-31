from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser

from api.models.propos.personnelles import Personnelles
from api.services.personnelles.propos.personnellesService import PersonnelleServices
from api.dto.personnelles.propos.personnellesDto import PersonnellesDTO

class PersonnelleController(APIView):
    # Indispensable pour recevoir des fichiers (Images/PDF)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, id=None):
        if id:
            try:
                personne = PersonnelleServices.getById(id)
                serializer = PersonnellesDTO(personne)
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except Personnelles.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": f"Personne non trouvée (ID: {id})"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            personnes = PersonnelleServices.getAll()
            serializer = PersonnellesDTO(personnes, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        # request.data contient à la fois les textes et les fichiers grâce aux parsers
        serializer = PersonnellesDTO(data=request.data)

        if serializer.is_valid():
            try:
                # On passe les données validées au service
                personne = PersonnelleServices.create(serializer.validated_data)
                
                return Response({
                    "status": "success",
                    "message": "Personnelle créée avec succès",
                    "data": PersonnellesDTO(personne).data
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
        try:
            # partial=True est la clé : il dit au Serializer 
            # de ne pas exiger TOUS les champs obligatoires
            serializer = PersonnellesDTO(data=request.data, partial=True)
            
            if serializer.is_valid():
                personne = PersonnelleServices.update(id, serializer.validated_data)
                return Response({
                    "status": "success",
                    "data": PersonnellesDTO(personne).data
                }, status=status.HTTP_200_OK)
            
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Personnelles.DoesNotExist:
            return Response({"message": "Non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    # --- AJOUTE CETTE MÉTHODE ---
    def patch(self, request, id):
        """Autorise explicitement la méthode PATCH en utilisant la logique du PUT"""
        return self.put(request, id)