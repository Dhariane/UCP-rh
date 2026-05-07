from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist

from api.models.auth.login.loginModel import Login
from api.services.auth.login.loginService import LoginService
from api.dto.auth.login.loginDto import LoginDTO

class LoginController(APIView):
    
    def post(self, request):
        email_saisi = request.data.get('email')
        password_saisi = request.data.get('password')

        # CAS 1 : CONNEXION
        if email_saisi and password_saisi and 'role' not in request.data:
            try:
                # 1. Recherche de l'utilisateur dans la table Login
                login_account = Login.objects.get(email__email=email_saisi)
                
                # 2. Vérification du mot de passe
                if check_password(password_saisi, login_account.password):
                    # 3. Création du user système pour le token
                    user_system, _ = User.objects.get_or_create(
                        username=email_saisi, 
                        email=email_saisi
                    )
                    
                    # 4. Génération du token
                    token, _ = Token.objects.get_or_create(user=user_system)
                    
                    # 5. Récupération de l'ID du personnel (CORRIGÉ ICI)
                    personnel_id = login_account.personnelle_id  # Accès direct au champ personnelle_id
                    
                    # 6. Réponse avec les bonnes données
                    return Response({
                        "status": "success",
                        "token": token.key,
                        "user": {
                            "personnel_id": personnel_id,  # Utilisation du bon ID
                            "email": email_saisi,
                            "role": login_account.role.name if login_account.role else "User"
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "error", 
                        "message": "Mot de passe incorrect"
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
            except Login.DoesNotExist:
                return Response({
                    "status": "error", 
                    "message": "Compte non trouvé"
                }, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({
                    "status": "error", 
                    "message": f"Erreur serveur : {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # CAS 2 : CRÉATION DE COMPTE
        serializer = LoginDTO(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": "error", 
                "message": "Erreur de validation des données"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        login_obj = LoginService.create(serializer.validated_data['email'])
        return Response({
            "status": "success", 
            "data": LoginDTO(login_obj).data
        }, status=status.HTTP_201_CREATED)