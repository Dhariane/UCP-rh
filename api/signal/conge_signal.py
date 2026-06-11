# api/signal/conge_signal.py

import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from api.models.conge.conge import Conge
from api.models.conge.notification import Notification
from api.models.fonction.contrat import Contrat
from api.models.auth.login.loginModel import Login


# ─────────────────────────────────────────────
# EMAIL EN ARRIÈRE-PLAN
# ─────────────────────────────────────────────
def _envoyer_email(destinataire_email: str, titre: str, message: str):
    try:
        html = f"""
        <html><body style="font-family: sans-serif; color: #333; padding: 20px;">
          <div style="max-width: 600px; margin: 0 auto; border: 1px solid #e0e0e0; border-radius: 8px; overflow: hidden;">
            <div style="background: #1a5c2a; padding: 20px; text-align: center;">
              <h1 style="color: white; margin: 0; font-size: 18px;">UCP Santé — Notification RH</h1>
            </div>
            <div style="padding: 24px;">
              <h2 style="color: #1a5c2a; font-size: 16px;">{titre}</h2>
              <p style="color: #555; line-height: 1.6;">{message}</p>
              <div style="text-align: center; margin-top: 24px;">
                <a href="http://localhost:3000/auth/login"
                   style="background: #1a5c2a; color: white; padding: 12px 24px;
                          text-decoration: none; border-radius: 6px; font-weight: bold;">
                  Accéder à l'application
                </a>
              </div>
            </div>
            <div style="background: #f5f5f5; padding: 12px; text-align: center;
                        font-size: 11px; color: #999;">
              UCP Santé — Message automatique, ne pas répondre.
            </div>
          </div>
        </body></html>
        """
        email = EmailMultiAlternatives(
            subject=titre,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[destinataire_email],
        )
        email.attach_alternative(html, "text/html")
        email.send(fail_silently=True)
        print(f"[EMAIL] ✅ Envoyé à {destinataire_email}")
    except Exception as e:
        print(f"[EMAIL] ❌ Erreur : {e}")


# ─────────────────────────────────────────────
# FONCTION CENTRALE : notif en base + email
# ─────────────────────────────────────────────
def _notifier(login, conge, type_notif: str, titre: str, message: str, metadata: dict):
    """Crée la notification en base ET envoie l'email en arrière-plan."""
    # 1. Notification en base
    Notification.objects.create(
        destinataire=login,
        conge=conge,
        type_notif=type_notif,
        titre=titre,
        message=message,
        metadata=metadata
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
        print(f"[EMAIL] Thread error : {e}")


# ─────────────────────────────────────────────
# ENVOI SELON L'ÉTAPE
# ─────────────────────────────────────────────
def envoi_notification_suivante(conge: Conge):
    try:
        etape = conge.etape_validation

        # ── CHEF ────────────────────────────────────────────────────────
        if etape == 'chef':
            contrat = Contrat.objects.filter(
                personnelle=conge.personnel, is_actif=True
            ).first()
            if contrat and contrat.fonction and contrat.fonction.chef_direct:
                contrat_chef = Contrat.objects.filter(
                    fonction=contrat.fonction.chef_direct, is_actif=True
                ).first()
                if contrat_chef:
                    login_chef = Login.objects.filter(
                        personnelle=contrat_chef.personnelle
                    ).first()
                    if login_chef:
                        _notifier(
                            login=login_chef,
                            conge=conge,
                            type_notif='validation_requise',
                            titre="Nouvelle demande de congé à valider",
                            message=(
                                f"{conge.personnel} a soumis une demande de congé "
                                f"de {conge.nombre_jours} jour(s). "
                                f"Votre validation est requise."
                            ),
                            metadata={"etape": "chef"}
                        )

        # ── GP/PF ────────────────────────────────────────────────────────
        elif etape == 'gp_pf':
            contrat_demandeur = Contrat.objects.filter(
                personnelle=conge.personnel, is_actif=True
            ).first()
            financement = contrat_demandeur.financement if contrat_demandeur else None

            if financement:
                logins_gp_pf = Login.objects.filter(
                    role__name__in=['GP', 'PF'],
                    personnelle__contrats__financement=financement,
                    personnelle__contrats__is_actif=True
                ).distinct()

                for login in logins_gp_pf:
                    _notifier(
                        login=login,
                        conge=conge,
                        type_notif='validation_requise',
                        titre=f"Demande de congé — {financement.nom}",
                        message=(
                            f"La demande de congé de {conge.personnel} "
                            f"({financement.nom}) attend votre validation."
                        ),
                        metadata={"etape": "gp_pf", "financement": financement.nom}
                    )
            else:
                # Pas de financement → notifier tous les GP/PF
                for login in Login.objects.filter(role__name__in=['GP', 'PF']):
                    _notifier(
                        login=login,
                        conge=conge,
                        type_notif='validation_requise',
                        titre="Demande de congé — GP/PF",
                        message=(
                            f"La demande de {conge.personnel} "
                            f"attend votre validation."
                        ),
                        metadata={"etape": "gp_pf"}
                    )

        # ── CN ───────────────────────────────────────────────────────────
        elif etape == 'cn':
            for login in Login.objects.filter(role__name='CN'):
                _notifier(
                    login=login,
                    conge=conge,
                    type_notif='validation_requise',
                    titre="Demande de congé — étape CN",
                    message=(
                        f"La demande de congé de {conge.personnel} "
                        f"attend votre validation (CN)."
                    ),
                    metadata={"etape": "cn"}
                )

        # ── RH ───────────────────────────────────────────────────────────
        elif etape == 'rh':
            for login in Login.objects.filter(role__name__in=['RH', 'admin']):
                _notifier(
                    login=login,
                    conge=conge,
                    type_notif='validation_requise',
                    titre="Demande de congé — validation finale RH",
                    message=(
                        f"La demande de congé de {conge.personnel} "
                        f"attend la validation finale RH."
                    ),
                    metadata={"etape": "rh"}
                )

        # ── TERMINÉ ──────────────────────────────────────────────────────
        elif etape == 'termine':
            login_demandeur = Login.objects.filter(
                personnelle=conge.personnel
            ).first()
            if login_demandeur:
                _notifier(
                    login=login_demandeur,
                    conge=conge,
                    type_notif='conge_approuve',
                    titre="Votre congé a été approuvé",
                    message=(
                        f"Votre demande de congé du {conge.date_debut} "
                        f"au {conge.date_fin} a été approuvée."
                    ),
                    metadata={"etape": "termine"}
                )

    except Exception as e:
        print(f"[SIGNAL] Erreur envoi_notification_suivante : {e}")


def envoi_notification_refus(conge: Conge, refuseur_login, motif: str = None):
    try:
        login_demandeur = Login.objects.filter(
            personnelle=conge.personnel
        ).first()
        if login_demandeur:
            message = (
                f"Votre demande de congé du {conge.date_debut} "
                f"au {conge.date_fin} a été refusée."
            )
            if motif:
                message += f"\n\nMotif : {motif}"

            _notifier(
                login=login_demandeur,
                conge=conge,
                type_notif='conge_refuse',
                titre="Votre congé a été refusé",
                message=message,
                metadata={
                    "etape": conge.etape_validation,
                    "refuse_par": str(refuseur_login),
                    "motif": motif or ""
                }
            )
    except Exception as e:
        print(f"[SIGNAL] Erreur envoi_notification_refus : {e}")


# ─────────────────────────────────────────────
# SIGNAL : création du congé uniquement
# ─────────────────────────────────────────────
@receiver(post_save, sender=Conge)
def initialiser_demande_conge(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        if instance.etape_validation == 'chef':
            envoi_notification_suivante(instance)

        elif instance.etape_validation == 'passation' and instance.passation_service:
            remplacant = instance.passation_service.remplacant
            if remplacant:
                login_remplacant = Login.objects.filter(
                    personnelle=remplacant
                ).first()
                if login_remplacant:
                    _notifier(
                        login=login_remplacant,
                        conge=instance,
                        type_notif='remplacement_requis',
                        titre="Demande de passation de service",
                        message=(
                            f"{instance.personnel} vous désigne comme remplaçant "
                            f"pour son congé du {instance.date_debut} "
                            f"au {instance.date_fin}."
                        ),
                        metadata={"etape": "passation"}
                    )
    except Exception as e:
        print(f"[SIGNAL] Erreur initialiser_demande_conge : {e}")