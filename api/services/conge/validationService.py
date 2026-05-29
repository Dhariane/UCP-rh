from django.utils import timezone
from api.models.conge.conge import Conge
from api.models.conge.validationConge import ValidationConge
from api.models.conge.statut import Statut
from api.models.conge.passationservice import PassationService
from api.models.fonction.contrat import Contrat
from api.models.fonction.fonctions import Fonctions
from api.models.auth.login.loginModel import Login


class ValidationService:

    # ─────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────

    @staticmethod
    def est_en_conge(personnelle) -> bool:
        today = timezone.now().date()
        return Conge.objects.filter(
            personnel=personnelle,
            statut_id=2,
            date_debut__lte=today,
            date_fin__gte=today
        ).exists()

    @staticmethod
    def get_remplacant(personnelle):
        passation = PassationService.objects.filter(
            titulaire=personnelle
        ).order_by('-date_absence').first()
        if passation and passation.remplacant:
            return Login.objects.filter(
                personnelle=passation.remplacant
            ).first()
        return None

    @staticmethod
    def get_login_disponible(login):
        if not login:
            return None
        if ValidationService.est_en_conge(login.personnelle):
            return ValidationService.get_remplacant(login.personnelle)
        return login

    @staticmethod
    def get_valideur_gp_rf(conge):
        fonction = Fonctions.objects.filter(
            personnelle=conge.personnel
        ).last()
        if not fonction:
            return None
        financement = fonction.financement.nom if fonction.financement else ""
        role_code   = 'GP' if financement == "Fond Mondial" else 'RF'
        login       = Login.objects.filter(role__name=role_code).first()
        return ValidationService.get_login_disponible(login)

    @staticmethod
    def get_chefs(conge):
        """Trouve le chef du même service que le personnel"""
        # Récupérer le contrat actuel du personnel
        from api.models.fonction.typeContrat import TypeContrats
        contrat = Contrat.objects.filter(
            personnelle=conge.personnel
        ).order_by('-dateDebut').first()

        if not contrat:
            return []

        # Trouver le chef du même service avec is_chef=True
        contrat_chef = Contrat.objects.filter(
            service        = contrat.service,
            fonction__is_chef = True,
            dateFin__isnull   = True  # contrat actif
        ).exclude(
            personnelle = conge.personnel  # pas lui-même
        ).first()

        if not contrat_chef:
            return []

        login_chef = Login.objects.filter(
            personnelle=contrat_chef.personnelle
        ).first()

        return [login_chef] if login_chef else []

    @staticmethod
    def cn_est_chef_direct(conge) -> bool:
        chefs = ValidationService.get_chefs(conge)
        return any(chef.role.name == 'Superadmin' for chef in chefs)

    @staticmethod
    def determiner_prochaine_etape(conge):
        if ValidationService.cn_est_chef_direct(conge):
            return 'rh'
        return 'gp_rf'

    # ─────────────────────────────────────────────
    # VALIDATION PRINCIPALE
    # ─────────────────────────────────────────────

    @staticmethod
    def valider(conge_id: int, login_id: int, decision: str, motif: str = None):
        conge       = Conge.objects.get(id=conge_id)
        login       = Login.objects.get(id=login_id)
        etape       = conge.etape_validation  # ← utilise etape_validation

        statut_approuve = Statut.objects.get(id=2)
        statut_refuse   = Statut.objects.get(id=3)

        # ── Étape CHEFS ──────────────────────────
        if etape == 'chef':
            chefs     = ValidationService.get_chefs(conge)
            chefs_ids = [c.id for c in chefs]

            if login.id not in chefs_ids:
                raise ValueError("Vous n'êtes pas chef de ce personnel")

            ValidationConge.objects.create(
                conge=conge, etape='chef',
                decision=decision, valideur=login, motif=motif
            )

            if decision == 'refuse':
                conge.statut          = statut_refuse
                conge.etape_validation = 'termine'
                conge.save()
                return conge

            # Vérifier si tous les chefs ont validé
            chefs_valides  = ValidationConge.objects.filter(
                conge=conge, etape='chef', decision='approuve'
            ).values_list('valideur_id', flat=True)

            chefs_restants = [c for c in chefs_ids if c not in chefs_valides]

            if chefs_restants:
                return conge  # on reste à l'étape chef

            # Tous validé → étape suivante
            conge.etape_validation = ValidationService.determiner_prochaine_etape(conge)
            conge.save()
            return conge

        # ── Étape GP/RF ──────────────────────────
        if etape == 'gp_rf':
            valideur_attendu = ValidationService.get_valideur_gp_rf(conge)
            if not valideur_attendu or login.id != valideur_attendu.id:
                raise ValueError("Vous n'êtes pas autorisé à valider cette étape")

            ValidationConge.objects.create(
                conge=conge, etape='gp_rf',
                decision=decision, valideur=login, motif=motif
            )

            if decision == 'refuse':
                conge.statut          = statut_refuse
                conge.etape_validation = 'termine'
            else:
                conge.etape_validation = 'cn'

            conge.save()
            return conge

        # ── Étape CN ─────────────────────────────
        if etape == 'cn':
            cn_login = Login.objects.filter(role__name='Superadmin').first()
            cn_login = ValidationService.get_login_disponible(cn_login)

            if not cn_login or login.id != cn_login.id:
                raise ValueError("Vous n'êtes pas autorisé à valider cette étape")

            ValidationConge.objects.create(
                conge=conge, etape='cn',
                decision=decision, valideur=login, motif=motif
            )

            if decision == 'refuse':
                conge.statut          = statut_refuse
                conge.etape_validation = 'termine'
            else:
                conge.etape_validation = 'rh'

            conge.save()
            return conge

        # ── Étape RH ─────────────────────────────
        if etape == 'rh':
            rh_login = Login.objects.filter(role__name='admin').first()  # ← admin
            rh_login = ValidationService.get_login_disponible(rh_login)

            if not rh_login or login.id != rh_login.id:
                raise ValueError("Vous n'êtes pas autorisé à valider cette étape")

            ValidationConge.objects.create(
                conge=conge, etape='rh',
                decision=decision, valideur=login, motif=motif
            )

            if decision == 'refuse':
                conge.statut          = statut_refuse
            else:
                conge.statut          = statut_approuve

            conge.etape_validation = 'termine'
            conge.save()
            return conge

        raise ValueError(f"Étape inconnue : {etape}")
