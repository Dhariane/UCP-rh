# api/signal/conge_signal.py  ← REMPLACE TOUT LE FICHIER

from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models.conge.conge import Conge          # ✅ import correct (plus depuis service)
from api.models.conge.notification import Notification
from api.models.fonction.contrat import Contrat
from api.models.auth.login.loginModel import Login


# ─────────────────────────────────────────────
# FONCTION CENTRALE : envoie la notif à la bonne
# personne selon l'étape courante du congé
# ─────────────────────────────────────────────
def envoi_notification_suivante(conge: Conge):
    """
    Lit conge.etape_validation et crée une Notification
    pour le bon destinataire.
    """
    try:
        etape = conge.etape_validation

        # ── ÉTAPE CHEF ──────────────────────────────────────────────────
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
                        Notification.objects.create(
                            destinataire=login_chef,
                            conge=conge,
                            type_notif='validation_requise',
                            titre="Nouvelle demande de congé à valider",
                            message=(
                                f"{conge.personnel} a soumis une demande de congé "
                                f"de {conge.nombre_jours} jour(s). Votre validation est requise."
                            ),
                            metadata={"etape": "chef"}
                        )

        # ── ÉTAPE GP/RF ──────────────────────────────────────────────────
        elif etape == 'gp_rf':
            # On notifie tous les utilisateurs ayant le rôle GP ou RF
            logins_gp_rf = Login.objects.filter(role__name__in=['GP', 'RF'])
            for login in logins_gp_rf:
                Notification.objects.create(
                    destinataire=login,
                    conge=conge,
                    type_notif='validation_requise',
                    titre="Demande de congé — étape GP/RF",
                    message=(
                        f"La demande de congé de {conge.personnel} "
                        f"attend votre validation (GP/RF)."
                    ),
                    metadata={"etape": "gp_rf"}
                )

        # ── ÉTAPE CN ────────────────────────────────────────────────────
        elif etape == 'cn':
            logins_cn = Login.objects.filter(role__name='CN')
            for login in logins_cn:
                Notification.objects.create(
                    destinataire=login,
                    conge=conge,
                    type_notif='validation_requise',
                    titre="Demande de congé — étape CN",
                    message=(
                        f"La demande de congé de {conge.personnel} "
                        f"attend votre validation (CN)."
                    ),
                    metadata={"etape": "cn"}
                )

        # ── ÉTAPE RH ────────────────────────────────────────────────────
        elif etape == 'rh':
            logins_rh = Login.objects.filter(role__name__in=['RH', 'admin'])
            for login in logins_rh:
                Notification.objects.create(
                    destinataire=login,
                    conge=conge,
                    type_notif='validation_requise',
                    titre="Demande de congé — étape RH (finale)",
                    message=(
                        f"La demande de congé de {conge.personnel} "
                        f"attend la validation finale RH."
                    ),
                    metadata={"etape": "rh"}
                )

        # ── TERMINÉ : notifier le demandeur ─────────────────────────────
        elif etape == 'termine':
            login_demandeur = Login.objects.filter(
                personnelle=conge.personnel
            ).first()
            if login_demandeur:
                Notification.objects.create(
                    destinataire=login_demandeur,
                    conge=conge,
                    type_notif='conge_approuve',
                    titre="Votre congé a été approuvé ✅",
                    message=(
                        f"Votre demande de congé du {conge.date_debut} "
                        f"au {conge.date_fin} a été approuvée."
                    ),
                    metadata={"etape": "termine"}
                )

    except Exception as e:
        print(f"[SIGNAL] Erreur envoi_notification_suivante : {e}")


def envoi_notification_refus(conge: Conge, refuseur_login):
    """Notifie le demandeur que son congé a été refusé."""
    try:
        login_demandeur = Login.objects.filter(personnelle=conge.personnel).first()
        if login_demandeur:
            Notification.objects.create(
                destinataire=login_demandeur,
                conge=conge,
                type_notif='conge_refuse',
                titre="Votre congé a été refusé ❌",
                message=(
                    f"Votre demande de congé du {conge.date_debut} "
                    f"au {conge.date_fin} a été refusée."
                ),
                metadata={"etape": conge.etape_validation, "refuse_par": str(refuseur_login)}
            )
    except Exception as e:
        print(f"[SIGNAL] Erreur envoi_notification_refus : {e}")


# ─────────────────────────────────────────────
# SIGNAL : à la CRÉATION du congé uniquement
# ─────────────────────────────────────────────
@receiver(post_save, sender=Conge)
def initialiser_demande_conge(sender, instance, created, **kwargs):
    if not created:
        return

    try:
        if instance.etape_validation == 'chef':
            # Congé 1 jour → notif directe au chef
            envoi_notification_suivante(instance)

        elif instance.etape_validation == 'passation' and instance.passation_service:
            remplacant = instance.passation_service.remplacant
            if remplacant:
                login_remplacant = Login.objects.filter(personnelle=remplacant).first()
                if login_remplacant:
                    Notification.objects.create(
                        destinataire=login_remplacant,
                        conge=instance,
                        type_notif='remplacement_requis',
                        titre="Demande de passation de service",
                        message=(
                            f"{instance.personnel} vous désigne comme remplaçant "
                            f"pour son congé du {instance.date_debut} au {instance.date_fin}."
                        ),
                        metadata={"etape": "passation"}
                    )
    except Exception as e:
        print(f"[SIGNAL] Erreur initialiser_demande_conge : {e}")