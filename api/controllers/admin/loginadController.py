from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from api.models.admin.loginadModel import Loginadmin
from api.services.admin.loginadService import LoginadminService
from api.dto.admin.loginadDto import LoginadminDTO

class LoginadminController(APIView):
    
    def post(self, request):
        email_saisi = request.data.get('email')
        password_saisi = request.data.get('password')

        # CAS 1 : CONNEXION (Pas de rôle dans la requête)
        if email_saisi and password_saisi and 'role' not in request.data:
            try:
                # 1. Recherche dans la table Loginadmin
                admin_account = Loginadmin.objects.get(email=email_saisi)
                
                # 2. Vérification du mot de passe
                if check_password(password_saisi, admin_account.password):
                    # 3. User système pour le token
                    user_system, _ = User.objects.get_or_create(
                        username=email_saisi, 
                        email=email_saisi
                    )
                    
                    # 4. Génération du token
                    token, _ = Token.objects.get_or_create(user=user_system)
                    
                    # 5. Réponse
                    return Response({
                        "status": "success",
                        "token": token.key,
                        "user": {
                            "id": admin_account.id,
                            "email": email_saisi,
                            "role": admin_account.role.name if admin_account.role else "Admin"
                        }
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "status": "error", 
                        "message": "Mot de passe incorrect"
                    }, status=status.HTTP_401_UNAUTHORIZED)
                    
            except Loginadmin.DoesNotExist:
                return Response({
                    "status": "error", 
                    "message": "Compte administrateur non trouvé"
                }, status=status.HTTP_401_UNAUTHORIZED)
            except Exception as e:
                return Response({
                    "status": "error", 
                    "message": f"Erreur serveur : {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # CAS 2 : CRÉATION DE COMPTE (Si le rôle est présent)
        serializer = LoginadminDTO(data=request.data)
        if not serializer.is_valid():
            return Response({
                "status": "error", 
                "message": "Erreur de validation des données",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            admin_obj = LoginadminService.create(serializer.validated_data)
            return Response({
                "status": "success", 
                "data": LoginadminDTO(admin_obj).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Erreur lors de la création : {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)