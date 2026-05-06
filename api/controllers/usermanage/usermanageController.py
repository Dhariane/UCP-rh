# api/controllers/auth/user/userManagementController.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.auth.login.loginModel import Login
from api.models.role.roleModel import Role

class UserManagementController(APIView):
    
    # GET: Pour lister les utilisateurs et les rôles dispo
    def get(self, request):
        try:
            # On utilise select_related pour optimiser la requête SQL (évite le N+1)
            users = Login.objects.select_related('role', 'email').all()
            
            data = [{
                "id": u.id,
                "email": u.email.email if u.email else "N/A",
                "role_id": u.role.id if u.role else None,
                "role_name": u.role.name if u.role else "User"
            } for u in users]
            
            # Liste des rôles pour remplir le <select> du front
            roles = Role.objects.all().values('id', 'name')
            
            return Response({
                "users": data,
                "available_roles": list(roles)
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({"error": f"Erreur lors de la récupération : {str(e)}"}, 
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH: Pour modifier le rôle
    def patch(self, request, id):
        try:
            user_account = Login.objects.get(id=id)
            role_id = request.data.get('role_id')
            
            if not role_id:
                return Response({"error": "role_id est requis"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Vérification de l'existence du rôle
            try:
                new_role = Role.objects.get(id=role_id)
            except Role.DoesNotExist:
                return Response({"error": "Le rôle spécifié n'existe pas"}, status=status.HTTP_404_NOT_FOUND)
            
            user_account.role = new_role
            user_account.save()
            
            return Response({
                "status": "success", 
                "message": f"Le rôle de {user_account.email.email} est désormais {new_role.name}"
            }, status=status.HTTP_200_OK)
            
        except Login.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)