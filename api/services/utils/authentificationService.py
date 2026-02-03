import jwt
from django.conf import settings
from rest_framework.permissions import BasePermission
class IsAuthenticatedJWT(BasePermission):
    def has_permission(self, request, view):
        # Récupérer le token depuis l'en-tête Authorization
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False

        token = auth_header.split(' ')[1]
        try:
            # Décoder le token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['id_membre']  # Ajouter l'ID utilisateur à la requête
            request.role=payload['role']
            return True
        except jwt.ExpiredSignatureError:
            return False  # Le token a expiré
        except jwt.InvalidTokenError:
            return False  # Le token est invalide

class HasRoleJWT(BasePermission):
    def has_permission(self, request, view):
        allowed_roles = getattr(view, "allowed_roles", [])

        return hasattr(request, "role") and request.role in allowed_roles
