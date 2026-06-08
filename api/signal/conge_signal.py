from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models.conge.conge import Conge
from api.models.conge.notification import Notification
from api.models.fonction.contrat import Contrat
from api.models.fonction.fonctions import Fonctions
from api.models.auth.login.loginModel import Login  # Ton modèle custom pour les utilisateurs
from api.services.conge.congeService import Conge

@receiver(post_save, sender=Conge)
def initialiser_demande_conge(sender, instance, created, **kwargs):
    """
    À la création de la demande de congé, on aiguille la première notification
    selon la durée du congé (1 jour ou plus).
    """
    if not created:
        return

    try:
        # CAS A : Le congé fait 1 seul jour -> On a sauté la passation, on alerte le chef direct
        if instance.etape_validation == 'chef':
            contrat = Contrat.objects.filter(personnelle=instance.personnel, is_actif=True).first()
            if contrat and contrat.fonction and contrat.fonction.chef_direct:
                chef_fonction = contrat.fonction.chef_direct
                contrat_chef = Contrat.objects.filter(fonction=chef_fonction, is_actif=True).first()
                
                if contrat_chef:
                    # Remplacement de personnel par personnelle selon ton modèle Login
                    login_chef = Login.objects.filter(personnelle=contrat_chef.personnelle).first()
                    if login_chef:
                        Notification.objects.create(
                            destinataire=login_chef,
                            conge=instance,
                            type_notif='validation_requise',
                            titre="🔔 Validation Chef requise (Congé 1j)",
                            message=f"Demande de congé d'un jour de {instance.personnel} en attente de votre accord.",
                            metadata={"etape": "chef"}
                        )
                        return
            
            # Sécurité : Si pas de chef direct, on pousse au CN
            instance.etape_validation = 'cn'
            instance.save(update_fields=['etape_validation'])
            envoi_notification_suivante(instance)

        # CAS B : Le congé fait 2 jours ou plus -> Circuit classique, notification au remplaçant
        elif instance.etape_validation == 'passation' and instance.passation_service:
            if instance.passation_service.remplacant:
                # 🚨 CORRECTION : Utilisation de 'personnelle' pour correspondre à ton modèle Login
                login_remplacant = Login.objects.filter(personnelle=instance.passation_service.remplacant).first()
                
                if login_remplacant:
                    Notification.objects.create(
                        destinataire=login_remplacant,
                        conge=instance,
                        type_notif='remplacement_requis',
                        titre="🔄 Validation de passation requise",
                        message=f"{instance.personnel} vous demande comme remplaçant pour sa passation de service ({instance.nombre_jours} jours).",
                        metadata={"etape": "passation"}
                    )
    except Exception as signal_error:
        # ✅ Évite de faire crasher l'enregistrement du congé si la notification échoue
        print(f"🚨 Erreur masquée dans le signal initialiser_demande_conge : {str(signal_error)}")