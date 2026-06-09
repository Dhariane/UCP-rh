# Dans loginService.py

import string
import secrets
import threading  # ✅ Ajout
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from api.models.auth.login.loginModel import Login
from api.dto.auth.login.loginDto import LoginDTO
from api.models.role.roleModel import Role


class LoginService:

    @staticmethod
    def generate_random_password(length=12):
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
    def _send_email_background(destinataire, raw_password):
        """Envoi email dans un thread séparé — ne bloque pas la requête."""
        try:
            print(f"📧 Tentative envoi à {destinataire}")
            print(f"📧 FROM : {settings.DEFAULT_FROM_EMAIL}")
            print(f"📧 CC : {[settings.DEFAULT_FROM_EMAIL, 'naly.fitahiana@gmail.com']}")
            print(f"📧 HOST : {settings.EMAIL_HOST}:{settings.EMAIL_PORT}")
            print(f"📧 TLS : {settings.EMAIL_USE_TLS} | SSL : {getattr(settings, 'EMAIL_USE_SSL', False)}")

            sujet = "Vos identifiants de connexion - UCP Santé"
            cc_addresses = [settings.DEFAULT_FROM_EMAIL, 'naly.fitahiana@gmail.com']

            message_texte = f"""
    Bienvenue sur la plateforme UCP Santé.

    Email        : {destinataire}
    Mot de passe : {raw_password}

    Accédez à la plateforme : https://ucp-rh-v1.vercel.app/auth/login
            """

            html_message = f"""
            <html>
              <body style="font-family: 'Segoe UI', sans-serif; color: #333; background-color: #f4f4f4; padding: 20px;">
                <div style="max-width:600px;margin:0 auto;background:#fff;border-radius:8px;overflow:hidden;border:1px solid #e0e0e0;">
                  <div style="background: linear-gradient(135deg, #8bc34a, #2e7d32); padding:30px; text-align:center;">
                    <h1 style="color:white;margin:0;font-size:22px;">Unité de Coordination des Projets_Santé</h1>
                    <p style="color:#e8f5e9;margin:5px 0 0;font-size:12px;">Plateforme RH</p>
                  </div>
                  <div style="padding:30px;">
                    <h2 style="color:#2c3e50;">Bienvenue,</h2>
                    <p>Votre compte a été créé par le service RH. Voici vos identifiants :</p>
                    <div style="background:#f9f9f9;border-left:4px solid #ff9800;padding:20px;margin:20px 0;border-radius:4px;">
                      <p style="margin:0;color:#666;font-size:14px;">Email :</p>
                      <p style="margin:5px 0 15px;font-weight:bold;font-size:16px;">{destinataire}</p>
                      <p style="margin:0;color:#666;font-size:14px;">Mot de passe :</p>
                      <p style="margin:5px 0 0;font-weight:bold;font-size:16px;font-family:monospace;">{raw_password}</p>
                    </div>
                    <div style="text-align:center;margin-top:25px;">
                      <a href="https://ucp-rh-v1.vercel.app/auth/login"
                        style="background:#2e7d32;color:white;padding:12px 25px;text-decoration:none;border-radius:5px;font-weight:bold;">
                        Accéder à la plateforme
                      </a>
                    </div>
                  </div>
                  <div style="background:#37474f;color:#cfd8dc;padding:15px;text-align:center;font-size:11px;">
                    <p style="margin:0;">UCP Santé — Message automatique, ne pas répondre.</p>
                  </div>
                </div>
              </body>
            </html>
            """

            email = EmailMultiAlternatives(
                subject=sujet,
                body=message_texte,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[destinataire],
                cc=cc_addresses,
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
            print(f"✅ Email envoyé à {destinataire}")

        except Exception as e:
            import traceback
            print(f"❌ Erreur envoi email : {e}")
            print(traceback.format_exc())

    @staticmethod
    def create(propos_instance):
        try:
            role = Role.objects.get(name="User")
        except Role.DoesNotExist:
            raise Exception("Rôle 'User' non trouvé.")  

        # 1. Génération du mot de passe
        raw_password = LoginService.generate_random_password()
        hashed_password = make_password(raw_password)
        destinataire = str(propos_instance.email)

        # 2. Création en base — rapide, pas de blocage
        login_obj = Login.objects.create(
            email=propos_instance,
            role=role,
            password=hashed_password
        )

        # 3. ✅ Email envoyé dans un thread séparé
        # La requête retourne immédiatement, l'email part en arrière-plan
        thread = threading.Thread(
            target=LoginService._send_email_background,
            args=(destinataire, raw_password),
            daemon=False 
        )
        thread.start()
        print(f"📧 Thread email lancé pour {destinataire}")

        return login_obj