# api/tasks.py

import threading
from django.utils import timezone
from api.models.conge.soldeConge import SoldeConge
from api.models.conge.notification import Notification
from api.models.auth.login.loginModel import Login
from api.signal.conge_signal import _envoyer_email


def rappel_solde_conge():
    """
    Vérifie tous les soldes de congé.
    Envoie une notification + email aux personnels
    ayant plus de 30 jours de solde restant.
    """
    print(f"[RAPPEL] Démarrage job rappel solde — {timezone.now()}")

    annee_courante = timezone.now().year

    # Récupérer tous les soldes > 30j pour l'année courante
    soldes = SoldeConge.objects.filter(
        annee=annee_courante,
        reste__gt=30
        
    ).select_related('personnel')

    count = 0
    for solde in soldes:
        personnel = solde.personnel

        # Trouver le login du personnel
        login = Login.objects.filter(personnelle=personnel).first()
        if not login:
            continue

        # Vérifier qu'on n'a pas déjà envoyé ce rappel cette semaine
        debut_semaine = timezone.now() - timezone.timedelta(days=7)
        deja_envoye = Notification.objects.filter(
            destinataire=login,
            type_notif='rappel_conge',
            date_creation__gte=debut_semaine
        ).exists()

        if deja_envoye:
            continue

        titre = "Pensez à prendre vos congés !"
        message = (
            f"Bonjour {personnel.prenom} {personnel.nom},\n\n"
            f"Vous avez actuellement {solde.reste} jours de congé disponibles. "
            f"Nous vous encourageons à planifier vos congés pour préserver "
            f"votre bien-être et respecter la politique de l'organisation.\n\n"
            f"N'hésitez pas à soumettre une demande de congé dès que possible."
        )

        # 1. Notification en base
        Notification.objects.create(
            destinataire=login,
            conge=None,
            type_notif='rappel_conge',
            titre=titre,
            message=message,
            metadata={"solde_restant": solde.reste, "annee": annee_courante}
        )

        # 2. Email en arrière-plan
        try:
            email_addr = str(login.email.email) if login.email else None
            if email_addr:
                thread = threading.Thread(
                    target=_envoyer_email,
                    args=(email_addr, titre, message),
                    daemon=False
                )
                thread.start()
        except Exception as e:
            print(f"[RAPPEL] Erreur email {personnel} : {e}")

        count += 1
        print(f"[RAPPEL] ✅ Notifié : {personnel} — {solde.reste} jours")

    print(f"[RAPPEL] Terminé — {count} personnel(s) notifié(s)")