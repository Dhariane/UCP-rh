import string
import secrets
from django.contrib.auth.hashers import make_password
from api.models.auth.login.loginModel import Login
from api.dto.auth.login.loginDto import LoginDTO
from django.core.mail import send_mail # envoye mail pour le mot de passe généré
from django.conf import settings
from api.models.role.roleModel import Role

class LoginService:

    @staticmethod
    def generate_random_password(length=12):
        """Génère un mot de passe aléatoire sécurisé."""
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(characters) for _ in range(length))

    @staticmethod
    def getAllDto():
        logins = Login.objects.all()
        return LoginDTO(logins, many=True)

    @staticmethod
    def getByIdDto(id):
        login = Login.objects.get(id=id)
        return LoginDTO(login)
      
    @staticmethod
    def create(propos_instance):
        
        try:
        
            role = Role.objects.get(name="User")  # Rôle par défaut
        except Role.DoesNotExist:
            raise Exception("Rôle 'User' non trouvé. Veuillez créer ce rôle avant de créer des logins.")
        # 1. Générer le mot de passe en clair
        raw_password = LoginService.generate_random_password()
        
        # 2. Hacher le mot de passe pour la base de données
        hashed_password = make_password(raw_password)
        
        # 3. Créer l'objet en base
        login_obj = Login.objects.create(
            email=propos_instance, 
            role=role,
            password=hashed_password
        )

        # --- PARTIE ENVOI D'EMAIL ---
        destinataire = propos_instance.email  # On récupère l'adresse mail
        sujet = "Vos identifiants de connexion - UCP RH"
        message = f"""
        Bonjour,
        
        Votre compte a été créé avec succès. 
        Voici vos identifiants :
        Email : {destinataire}
        Mot de passe : {raw_password}
        
        Veuillez changer votre mot de passe après votre première connexion.
        """
        
        try:
            send_mail(
                sujet,
                message,
                settings.EMAIL_HOST_USER, # Votre email d'expédition (configuré dans settings.py)
                [destinataire],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Erreur d'envoi d'email : {e}")
        # ----------------------------

        return login_obj