from django.utils import timezone
from api.models.conge.conge import Conge
from api.models.conge.validationConge import ValidationConge
from api.models.conge.statut import Statut
from api.models.conge.passationservice import PassationService
from api.models.fonction.contrat import Contrat
from api.models.auth.login.loginModel import Login


class ValidationService:

    # ─────────────────────────────────────────────
    # 1. HELPERS DE VÉRIFICATION & DISPONIBILITÉ
    # ─────────────────────────────────────────────

    @staticmethod
    def est_en_conge(personnel_obj) -> bool:
        """Vérifie si un employé est actuellement en congé validé"""
        today = timezone.now().date()
        return Conge.objects.filter(
            personnel=personnel_obj,
            statut_id=2,
            date_debut__lte=today,
            date_fin__gte=today
        ).exists()

    @staticmethod
    def get_remplacant(personnel_obj):
        """Récupère le compte Login du remplaçant d'un personnel absent"""
        passation = PassationService.objects.filter(
            titulaire=personnel_obj
        ).order_by('-date_absence').first()
        if passation and passation.remplacant:
            return Login.objects.filter(
                personnelle=passation.remplacant
            ).first()
        return None

    @staticmethod
    def get_login_disponible(login):
        """Si le valideur est en congé, retourne le compte de son remplaçant"""
        if not login:
            return None
        if login.personnelle and ValidationService.est_en_conge(login.personnelle):
            remplacant_login = ValidationService.get_remplacant(login.personnelle)
            return remplacant_login if remplacant_login else login
        return login

    # ─────────────────────────────────────────────
    # 2. HELPERS D'AIGUILLAGE DU WORKFLOW
    # ─────────────────────────────────────────────

    @staticmethod
    def get_chefs(conge):
        """Trouve le login du chef direct du demandeur via son contrat actif"""
        # On cherche le contrat actif du demandeur
        contrat = Contrat.objects.filter(
            personnelle=conge.personnel,  # Vérifie si ton modèle Contrat utilise 'personnel' ou 'personnelle' ici
            is_actif=True
        ).first()

        if not contrat or not contrat.fonction or not contrat.fonction.chef_direct:
            return []

        chef_fonction = contrat.fonction.chef_direct

        # Trouver le contrat actif de la personne qui occupe cette fonction de chef
        contrat_chef = Contrat.objects.filter(
            fonction=chef_fonction,
            is_actif=True
        ).first()

        if not contrat_chef:
            return []

        login_chef = Login.objects.filter(
            personnelle=contrat_chef.personnelle
        ).first()

        return [login_chef] if login_chef else []

    @staticmethod
    def get_valideur_gp_rf(conge):
        """Détermine si le valideur budgétaire est un GP ou un Point Focal (RF)"""
        contrat = Contrat.objects.filter(
            personnelle=conge.personnel,
            is_actif=True
        ).first()
        
        if not contrat or not contrat.financement:
            return None
            
        financement = contrat.financement.nom.upper()
        
        # Choix du rôle selon le financement rattaché au contrat
        role_code = 'GP' if "FONDS MONDIAL" in financement or "FOND MONDIAL" in financement else 'RF'
        
        login = Login.objects.filter(role__name=role_code).first()
        return ValidationService.get_login_disponible(login)

    @staticmethod
    def cn_est_chef_direct(conge) -> bool:
        """Vérifie si le demandeur dépend directement du Coordinateur National (Superadmin)"""
        chefs = ValidationService.get_chefs(conge)
        return any(chef.role.name == 'Superadmin' for chef in chefs)

    # ─────────────────────────────────────────────
    # 3. MÉTHODE PRINCIPALE DE VALIDATION
    # ─────────────────────────────────────────────

    @staticmethod
    def valider(conge_id: int, login_id: int, decision: str, motif: str = None):
        conge = Conge.objects.get(id=conge_id)
        login = Login.objects.get(id=login_id)
        etape = conge.etape_validation

        # ── ÉTAPE CHEF DIRECT ─────────────────
        if etape == 'chef':
            chefs = ValidationService.get_chefs(conge)
            if not chefs:
                raise ValueError("Aucun chef direct assigné à votre fonction.")
                
            chef_attendu = ValidationService.get_login_disponible(chefs[0])
            if login.id != chef_attendu.id:
                raise ValueError("Vous n'êtes pas autorisé à valider cette étape hiérarchique.")

            ValidationConge.objects.create(
                conge=conge, etape='chef',
                decision=decision, valideur=login, motif=motif
            )
            conge.refresh_from_db()
            return conge

        # ── ÉTAPE GP / RF (FINANCEMENT) ───────
        elif etape == 'gp_rf':
            valideur_attendu = ValidationService.get_valideur_gp_rf(conge)
            if not valideur_attendu or login.id != valideur_attendu.id:
                raise ValueError("Vous n'êtes pas autorisé à valider le financement de cette étape.")

            label_etape = 'gp' if valideur_attendu.role.name == 'GP' else 'rf'

            ValidationConge.objects.create(
                conge=conge, etape=label_etape,
                decision=decision, valideur=login, motif=motif
            )
            conge.refresh_from_db()
            return conge

        # ── ÉTAPE CN (COORDINATEUR NATIONAL) ──
        elif etape == 'cn':
            cn_login = Login.objects.filter(role__name='Superadmin').first()
            cn_login = ValidationService.get_login_disponible(cn_login)

            if not cn_login or login.id != cn_login.id:
                raise ValueError("Seul le Coordinateur National (Superadmin) peut valider cette étape.")

            ValidationConge.objects.create(
                conge=conge, etape='cn',
                decision=decision, valideur=login, motif=motif
            )
            conge.refresh_from_db()
            return conge

        # ── ÉTAPE RH (RESSOURCES HUMAINES) ────
        elif etape == 'rh':
            rh_login = Login.objects.filter(role__name='admin').first()
            rh_login = ValidationService.get_login_disponible(rh_login)

            if not rh_login or login.id != rh_login.id:
                raise ValueError("Seul un administrateur des Ressources Humaines peut clore cette étape.")

            ValidationConge.objects.create(
                conge=conge, etape='rh',
                decision=decision, valideur=login, motif=motif
            )
            conge.refresh_from_db()
            return conge

        raise ValueError(f"Étape inconnue : {etape}")
