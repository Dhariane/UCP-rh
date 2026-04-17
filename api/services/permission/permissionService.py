from django.db import transaction
from django.core.exceptions import ValidationError

class PermissionService:
    @staticmethod
    def calculer_duree(date_debut, date_fin):
        diff = date_fin - date_debut
        return max(0, diff.days + (diff.seconds / 86400))

    @staticmethod
    @transaction.atomic
    def approuver_permission(permission_id):
        permission = Permissions.objects.get(id=permission_id)
        
        if permission.statut == 'Approuvé':
            return permission

        personne = permission.personnelle
        duree_calculee = PermissionService.calculer_duree(permission.date_debut, permission.date_fin)

        if personne.solde_jours >= duree_calculee:
            # 1. On enregistre la photo du solde au moment de l'approbation
            permission.solde_initial = personne.solde_jours
            permission.duree = duree_calculee
            permission.solde_restant = personne.solde_jours - duree_calculee
            
            # 2. On met à jour le solde réel de l'employé
            personne.solde_jours = permission.solde_restant
            
            permission.statut = 'Approuvé'
            
            personne.save()
            permission.save()
            return permission
        else:
            raise ValidationError(f"Solde insuffisant. Disponible: {personne.solde_jours}")