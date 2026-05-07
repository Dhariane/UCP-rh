from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def envoyer_email(destinataire, sujet, corps_texte, corps_html=None):
    try:
        # Création de l'email
        email = EmailMultiAlternatives(
            subject=sujet,
            body=corps_texte,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[destinataire],
        )

        # Si tu veux aussi envoyer une version HTML
        if corps_html:
            email.attach_alternative(corps_html, "text/html")

        # Envoi du mail
        email.send(fail_silently=False)
        print("✅ Email envoyé avec succès.")

    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de l'email : {e}")

    

def envoyer_code_validation(destinataire, code):
    sujet = "Code de validation chez edodrandria"

    corps_texte = f"Bonjour, merci de nous avoir rejoint edodrandria company."
    corps_html = f"""
    <html>
        <body>
            <h1 style="color: blue;">Bienvenue !</h1>
            <p>Votre code de validation est : <strong>{code}</strong></p>
            <p>Cordialement,<br>L'équipe</p>
        </body>
    </html>
    """

    envoyer_email(destinataire, sujet, corps_texte, corps_html)

