from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.utils.jwtService import creer_token_jwt
class LoginController(APIView):
    """
    Controller pour tester la création du token JWT
    """

    def post(self, request):
        # 🎯 Simule un utilisateur (normalement venant de la BD)
        claims = {
            "id_membre": 1,
            "role": "ADMIN",
            "email": "test@test.com"
        }

        token = creer_token_jwt(claims)

        return Response({
            "token": token
        }, status=status.HTTP_200_OK)
