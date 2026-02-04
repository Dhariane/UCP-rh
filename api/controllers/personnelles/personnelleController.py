from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.utils.authentificationService import IsAuthenticatedJWT, HasRoleJWT
class PersonnelleController(APIView):
    """
    Controller pour la gestion du personnelle
    """

    permission_classes = [IsAuthenticatedJWT, HasRoleJWT]
    allowed_roles = ["ADMIN"]  # 👈 ici tu définis les rôles autorisés

    def get(self, request):
        """
        Récupérer les infos du personnelle connecté
        """
        return Response({
            "message": "Informations personnelles",
            "id_membre": request.user_id,
            "role": request.role
        }, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Création d'un personnelle (exemple)
        """
        data = request.data

        nom = data.get("nom")
        prenom = data.get("prenom")

        if not nom or not prenom:
            return Response({
                "error": "nom et prenom sont obligatoires"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Simulation insertion BD
        personnelle = {
            "id": 1,
            "nom": nom,
            "prenom": prenom
        }

        return Response({
            "message": "Personnelle créé avec succès",
            "data": personnelle
        }, status=status.HTTP_201_CREATED)
