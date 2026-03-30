import string
import secrets
import os
from django.contrib.auth.hashers import make_password
from api.models.auth.login.loginModel import Login
from api.dto.auth.login.loginDto import LoginDTO
from django.core.mail import EmailMultiAlternatives # Changé pour supporter le logo
from django.conf import settings
from api.models.role.roleModel import Role
from django.utils.html import strip_tags
from email.mime.image import MIMEImage # Pour l'image

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
            role = Role.objects.get(name="User")
        except Role.DoesNotExist:
            raise Exception("Rôle 'User' non trouvé.")

        # 1. Préparation des identifiants
        raw_password = LoginService.generate_random_password()
        hashed_password = make_password(raw_password)
        destinataire = propos_instance.email 

        # 2. Création en base de données
        login_obj = Login.objects.create(
            email=propos_instance, 
            role=role,
            password=hashed_password
        )

        # --- PARTIE EMAIL AVEC LOGO ET CSS ---
        sujet = "Vos identifiants de connexion - UCP Santé"
        
        # Template HTML avec ajout du logo via CID
        html_message = f"""
        <html>
            <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; overflow: hidden; border: 1px solid #e0e0e0; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
                    
                    <div style="background: linear-gradient(135deg, #8bc34a 0%, #2e7d32 100%); padding: 30px; text-align: center;">
                        <img src="cid:logo_ucp" alt="Logo UCP" style="height: 80px; margin-bottom: 15px; border-radius: 5px;">
                        <h1 style="color: white; margin: 0; font-size: 24px; letter-spacing: 1px;">Unité de Coordination des Projets_Santé</h1>
                        <p style="color: #e8f5e9; margin: 5px 0 0 0; font-size: 12px; text-transform: uppercase;">Plateforme de Gestion des Ressources Humaines</p>
                    </div>

                    <div style="padding: 30px;">
                        <h2 style="color: #2c3e50; margin-top: 0;">Bienvenue,</h2>
                        <p>Votre compte a été créé avec succès par le service RH. Voici vos paramètres de connexion sécurisés :</p>
                        
                        <div style="background-color: #f9f9f9; border-left: 4px solid #ff9800; padding: 20px; margin: 25px 0; border-radius: 4px;">
                            <p style="margin: 0; font-size: 14px; color: #666;">Email :</p>
                            <p style="margin: 5px 0 15px 0; font-weight: bold; font-size: 16px; color: #212121;">{destinataire}</p>
                            
                            <p style="margin: 0; font-size: 14px; color: #666;">Mot de passe :</p>
                            <p style="margin: 5px 0 0 0; font-weight: bold; font-size: 16px; color: #252F3D; font-family: monospace;">{raw_password}</p>
                        </div>

                        <p style="font-size: 13px; color: #7f8c8d;">
                            <strong>Note :</strong> Pour des raisons de sécurité, nous vous recommandons de bien garder ce mail pour ne pas perdre le mot de passe.
                        </p>

                        <div style="text-align: center; margin-top: 30px;">
                            <a href="http://192.168.0.100:3000/auth/login" style="background-color: #2e7d32; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">Accéder à la plateforme</a>
                        </div>
                    </div>

                    <div style="background-color: #37474f; color: #cfd8dc; padding: 15px; text-align: center; font-size: 11px;">
                        <p style="margin: 0;">Unité de Coordination des Projets_Santé - UCP</p>
                        <p style="margin: 5px 0 0 0;">Ceci est un message automatique, merci de ne pas y répondre.</p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        plain_message = strip_tags(html_message)

        try:
            # Configuration de l'email
            email = EmailMultiAlternatives(
                sujet,
                plain_message,
                settings.EMAIL_HOST_USER,
                [destinataire]
            )
            email.attach_alternative(html_message, "text/html")

            # --- LOGIQUE D'ATTACHEMENT DU LOGO ---
            logo_path = os.path.join(settings.BASE_DIR, 'api', 'static', 'ucp.jpeg')
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                logo = MIMEImage(logo_data)
                logo.add_header('Content-ID', '<logo_ucp>') # Doit correspondre à cid:logo_ucp dans le HTML
                email.attach(logo)
            # ------------------------------------

            email.send(fail_silently=False)
        except Exception as e:
            print(f"Erreur d'envoi d'email : {e}")

        return login_obj