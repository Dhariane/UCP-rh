from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User # Ne t'inquiète pas, il existe par défaut !
from django.contrib.auth.hashers import check_password # Pour comparer les mots de passe hachés

from api.models.auth.login.loginModel import Login
from api.services.auth.login.loginService import LoginService
from api.dto.auth.login.loginDto import LoginDTO

class LoginController(APIView):
    
    def post(self, request):
        email_saisi = request.data.get('email')
        password_saisi = request.data.get('password')

        # CAS 1 : CONNEXION (Authentification via ton modèle Login)
        if email_saisi and password_saisi and 'role' not in request.data:
            try:
                # 1. On cherche l'utilisateur dans TA table Login
                # email__email car Login.email est une clé étrangère vers Propos/Personnel
                login_account = Login.objects.get(email__email=email_saisi)
                
                # 2. On compare le mot de passe haché de ta base avec celui saisi
                if check_password(password_saisi, login_account.password):
                    
                    # 3. On crée/récupère un utilisateur système "fantôme" pour le Token
                    # Django Rest Framework a besoin de cet objet User pour créer le token
                    user_system, _ = User.objects.get_or_create(
                        username=email_saisi, 
                        email=email_saisi
                    )
                    
                    token, _ = Token.objects.get_or_create(user=user_system)
                    
                    return Response({
                        "status": "success",
                        "token": token.key,
                        "user": {
                            "id": login_account.id,              # ID de la table Login
                            "personnel_id": getattr(login_account.email, 'id', None), # ID de l'employé (via la FK email)
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
                return Response({"status": "error", 
                                 "message": "Compte non trouvé"
                                 }, status=status.HTTP_401_UNAUTHORIZED)

        # CAS 2 : CRÉATION (Ton code d'origine reste ici)
        serializer = LoginDTO(data=request.data)
        if not serializer.is_valid():
            return Response({"status": "error", 
                             "message": "Erreur validation"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        login_obj = LoginService.create(serializer.validated_data['email'])
        return Response({"status": "success", "data": LoginDTO(login_obj).data}, status=status.HTTP_201_CREATED)

    # ... reste de tes méthodes (GET, PUT)