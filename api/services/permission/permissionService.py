from django.utils import timezone
from api.models.permission.permissionModel import Permissions, SoldePermission


class PermissionService:

    # ------------------------------------------------------------------
    # Calcul durée en jours ouvrables (simple soustraction pour l'instant)
    # ------------------------------------------------------------------
    @staticmethod
    def calculer_duree(date_debut, date_fin):
        delta = date_fin - date_debut
        duree = delta.days + 1  # inclus le jour de début
        return max(duree, 0)

    # ------------------------------------------------------------------
    # Récupère ou crée le SoldePermission de l'employé pour une année
    # ------------------------------------------------------------------
    @staticmethod
    def get_or_create_solde(personnelle, annee=None):
        if annee is None:
            annee = timezone.now().year
        solde, _ = SoldePermission.objects.get_or_create(
            personnelle=personnelle,
            annee=annee,
            defaults={'solde_disponible': SoldePermission.SOLDE_MAX}
        )
        return solde

    # ------------------------------------------------------------------
    # Approbation : déduit la durée du solde
    # ------------------------------------------------------------------
    @staticmethod
    def approuver_permission(permission_id):
        permission = Permissions.objects.select_related(
            'personnelle', 'evenement'
        ).get(id=permission_id)

        if permission.statut != 'En attente':
            raise Exception(f"Cette permission est déjà '{permission.statut}'.")

        annee = permission.date_debut.year
        solde = PermissionService.get_or_create_solde(permission.personnelle, annee)

        if solde.solde_disponible < permission.duree:
            raise Exception(
                f"Solde insuffisant : {solde.solde_disponible}j disponible, "
                f"{permission.duree}j demandé."
            )

        # Déduction
        solde.solde_disponible -= permission.duree
        solde.save()

        permission.statut = 'Approuvé'
        permission.solde_initial = solde.solde_disponible + permission.duree  # avant déduction
        permission.solde_restant = solde.solde_disponible
        permission.save()

        return permission

    # ------------------------------------------------------------------
    # Refus : ne touche pas au solde
    # ------------------------------------------------------------------
    @staticmethod
    def refuser_permission(permission_id):
        permission = Permissions.objects.get(id=permission_id)

        if permission.statut != 'En attente':
            raise Exception(f"Cette permission est déjà '{permission.statut}'.")

        permission.statut = 'Refusé'
        permission.save()
        return permission

    # ------------------------------------------------------------------
    # Réinitialisation du solde à 10j (action RH)
    # ------------------------------------------------------------------
    @staticmethod
    def reinitialiser_solde(personnelle_id, annee=None):
        if annee is None:
            annee = timezone.now().year

        solde = SoldePermission.objects.filter(
            personnelle_id=personnelle_id,
            annee=annee
        ).first()

        if not solde:
            raise Exception(f"Aucun solde trouvé pour cette année ({annee}).")

        solde.reinitialiser()
        return solde