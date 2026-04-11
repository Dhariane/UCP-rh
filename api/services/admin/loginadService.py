from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from api.models.admin.loginadModel import Loginadmin

class LoginadminService:
    @staticmethod
    def create(data): # Renommé en 'create' pour correspondre au controller
        """Crée un admin avec un mot de passe sécurisé."""
        return Loginadmin.objects.create(
            email=data['email'],
            password=make_password(data['password']),
            role=data['role']
        )

    @staticmethod
    def list_all_admins():
        return Loginadmin.objects.all().select_related('role')

    @staticmethod
    def delete_admin(admin_id):
        admin = get_object_or_404(Loginadmin, id=admin_id)
        admin.delete()
        return True