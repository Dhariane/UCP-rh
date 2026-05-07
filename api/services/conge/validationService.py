from django.utils import timezone
from api.models.conge.conge import Conge
from api.models.conge.validationConge import ValidationConge
from api.models.conge.statut import Statut
from api.models.conge.passationservice import PassationService
from api.models.fonction.fonctions import Fonctions
from api.models.auth.login.loginModel import Login


class ValidationService:

    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────

    @staticmethod
    def est_en_conge(personnelle) -> bool:
        """Vérifie si un personnel est en congé approuvé aujourd'hui"""
        today = timezone.now().date()
        return Conge.objects.filter(
            personnel=personnelle,
            statut__statut='approuve',
            date_debut__lte=today,
            date_fin__gte=today
        ).exists()

    @staticmethod
    def get_remplacant(personnelle):
        """Retourne le remplaçant d'un personnel depuis sa passation"""
        passation = PassationService.objects.filter(
            titulaire=personnelle
        ).order_by('-date_absence').first()

        if passation and passation.remplacant:
            login = Login.objects.filter(
                personnelle=passation.remplacant
            ).first()
            return login
        return None

    @staticmethod
    def get_login_disponible(login):
        """Retourne le login ou son remplaçant s'il est en congé"""
        if not login:
            return None
        if ValidationService.est_en_conge(login.personnelle):
            return ValidationService.get_remplacant(login.personnelle)
        return login

    @staticmethod
    def get_valideur_gp_rf(conge):
        """Retourne GP ou RF selon le financement du personnel"""
        fonction = Fonctions.objects.filter(
            personnelle=conge.personnel
        ).last()

        if not fonction:
            return None

        financement = fonction.financement.nom if fonction.financement else ""

        if financement == "Fonds Mondial":
            role_code = 'GP'
        else:
            role_code = 'RF'

        login = Login.objects.filter(role__name=role_code).first()
        return ValidationService.get_login_disponible(login)

    @staticmethod
    def get_chefs(conge):
        """Retourne tous les chefs directs du personnel"""
        fonction = Fonctions.objects.filter(
            personnelle=conge.personnel
        ).last()

        if not fonction:
            return []

        return list(fonction.superieurs.all())

    @staticmethod
    def cn_est_chef_direct(conge) -> bool:
        """Vérifie si le CN est un chef direct du personnel"""
        chefs = ValidationService.get_chefs(conge)
        return any(chef.role.name == 'CN' for chef in chefs)

    @staticmethod
    def determiner_prochaine_etape(conge):
        """
        Détermine le prochain statut après validation de tous les chefs.
        Si CN est chef direct → saute GP/RF et CN → va direct RH
        Sinon → flux normal GP/RF → CN → RH
        """
        if ValidationService.cn_est_chef_direct(conge):
            return 'attente_rh'
        return 'attente_gp_rf'

    # ─────────────────────────────────────────────
    # VALIDATION PRINCIPALE
    # ─────────────────────────────────────────────

    @staticmethod
    def valider(conge_id: int, login_id: int, decision: str, motif: str = None):
        """Valider ou refuser une étape du congé"""
        conge   = Conge.objects.get(id=conge_id)
        login   = Login.objects.get(id=login_id)
        statut_code = conge.statut.statut

        # ── Étape CHEFS ──────────────────────────
        if statut_code == 'attente_chef':

            chefs = ValidationService.get_chefs(conge)
            chefs_ids = [c.id for c in chefs]

            # Vérifier que ce login est bien un chef de ce personnel
            if login.id not in chefs_ids:
                raise ValueError("Vous n'êtes pas chef de ce personnel")

            # Enregistrer la validation de ce chef
            ValidationConge.objects.create(
                conge    = conge,
                etape    = 'chef',
                decision = decision,
                valideur = login,
                motif    = motif,
            )

            if decision == 'refuse':
                conge.statut = Statut.objects.get(statut='refuse')
                conge.save()
                return conge

            # Vérifier si tous les chefs ont validé
            chefs_qui_ont_valide = ValidationConge.objects.filter(
                conge    = conge,
                etape    = 'chef',
                decision = 'approuve'
            ).values_list('valideur_id', flat=True)

            chefs_restants = [
                c for c in chefs_ids
                if c not in chefs_qui_ont_valide
            ]

            if chefs_restants:
                # Pas encore tous validé → on reste à attente_chef
                return conge

            # Tous les chefs ont validé → étape suivante
            prochain_statut = ValidationService.determiner_prochaine_etape(conge)
            conge.statut = Statut.objects.get(statut=prochain_statut)
            conge.save()
            return conge

        # ── Étape GP/RF ──────────────────────────
        if statut_code == 'attente_gp_rf':
            valideur_attendu = ValidationService.get_valideur_gp_rf(conge)

            if not valideur_attendu or login.id != valideur_attendu.id:
                raise ValueError("Vous n'êtes pas autorisé à valider cette étape")

            ValidationConge.objects.create(
                conge    = conge,
                etape    = 'gp_rf',
                decision = decision,
                valideur = login,
                motif    = motif,
            )

            if decision == 'refuse':
                conge.statut = Statut.objects.get(statut='refuse')
            else:
                conge.statut = Statut.objects.get(statut='attente_cn')

            conge.save()
            return conge

        # ── Étape CN ─────────────────────────────
        if statut_code == 'attente_cn':
            cn_login = Login.objects.filter(role__name='CN').first()
            cn_login = ValidationService.get_login_disponible(cn_login)

            if not cn_login or login.id != cn_login.id:
                raise ValueError("Vous n'êtes pas autorisé à valider cette étape")

            ValidationConge.objects.create(
                conge    = conge,
                etape    = 'cn',
                decision = decision,
                valideur = login,
                motif    = motif,
            )

            if decision == 'refuse':
                conge.statut = Statut.objects.get(statut='refuse')
            else:
                conge.statut = Statut.objects.get(statut='attente_rh')

            conge.save()
            return conge

        # ── Étape RH ─────────────────────────────
        if statut_code == 'attente_rh':
            rh_login = Login.objects.filter(role__name='RH').first()
            rh_login = ValidationService.get_login_disponible(rh_login)

            if not rh_login or login.id != rh_login.id:
                raise ValueError("Vous n'êtes pas autorisé à valider cette étape")

            ValidationConge.objects.create(
                conge    = conge,
                etape    = 'rh',
                decision = decision,
                valideur = login,
                motif    = motif,
            )

            if decision == 'refuse':
                conge.statut = Statut.objects.get(statut='refuse')
            else:
                conge.statut = Statut.objects.get(statut='approuve')

            conge.save()
            return conge

        raise ValueError(f"Statut inconnu : {statut_code}")