<<<<<<< HEAD
# api/services/conge/congeService.py  ← REMPLACE TOUT LE FICHIER

from api.models.conge.conge import Conge
from api.models.conge.statut import Statut
from api.models.fonction.contrat import Contrat


# Ordre des étapes (hors passation qui est gérée séparément)
ETAPES_ORDRE = ['chef', 'gp_rf', 'cn', 'rh', 'termine']


def _etape_suivante(conge: Conge) -> str:
    """
    Retourne l'étape suivante selon le workflow.
    Règle métier : si le CN est le chef direct du demandeur,
    on saute gp_rf.
    """
    etape_actuelle = conge.etape_validation

    # Récupérer le contrat actif du demandeur
    contrat = Contrat.objects.filter(
        personnelle=conge.personnel, is_actif=True
    ).first()

    # Vérifier si le CN est le chef direct (règle métier qui saute gp_rf)
    cn_est_chef_direct = False
    if contrat and contrat.fonction and contrat.fonction.chef_direct:
        from api.models.auth.login.loginModel import Login
        chef_direct_logins = Login.objects.filter(
            personnelle__contrats__fonction=contrat.fonction.chef_direct,
            role__name='CN'
        )
        cn_est_chef_direct = chef_direct_logins.exists()

    etapes = ETAPES_ORDRE.copy()
    if cn_est_chef_direct and 'gp_rf' in etapes:
        etapes.remove('gp_rf')  # On saute gp_rf

    try:
        idx = etapes.index(etape_actuelle)
        return etapes[idx + 1] if idx + 1 < len(etapes) else 'termine'
    except ValueError:
        return 'termine'


class CongeServices:

    @staticmethod
    def getAll():
        return Conge.objects.all().order_by("-created_at")

    @staticmethod
    def getById(id: int) -> Conge:
        return Conge.objects.get(id=id)

    @staticmethod
    def getByPersonnel(personnel_id: int):
        return Conge.objects.filter(personnel_id=personnel_id).order_by("-created_at")

    @staticmethod
    def getEnAttente():
        return Conge.objects.filter(statut__code='en_attente').order_by("-created_at")

    @staticmethod
    def create(data) -> Conge:
        try:
            statut_attente = Statut.objects.get(id=1)
        except Statut.DoesNotExist:
            raise ValueError("Le statut initial (ID: 1) n'existe pas.")

        conge = Conge.objects.create(
            personnel=data.get('personnel'),
            type_conge=data.get('type_conge'),
            solde_conge=data.get('solde_conge'),
            date_debut=data.get('date_debut'),
            date_fin=data.get('date_fin'),
            description=data.get('description'),
            passation_service=data.get('passation_service'),
            statut=statut_attente,
            validated_by=data.get('validated_by')
        )
        return conge

    @staticmethod
    def update(id: int, data) -> Conge:
        conge = Conge.objects.get(id=id)
        for field, value in data.items():
            if value is not None and hasattr(conge, field):
                setattr(conge, field, value)
        conge.save()
        return conge

    @staticmethod
    def delete(id: int) -> bool:
        conge = Conge.objects.get(id=id)
        conge.delete()
        return True

    # ──────────────────────────────────────────────────────────────────
    # WORKFLOW PRINCIPAL
    # ──────────────────────────────────────────────────────────────────

    @staticmethod
    def valider_etape(conge_id: int, validated_by_login) -> Conge:
        """
        Fait avancer le congé à l'étape suivante.
        Met le statut à 'approuve' uniquement quand on arrive à 'termine'.
        """
        from api.signal.conge_signal import envoi_notification_suivante

        conge = Conge.objects.get(id=conge_id)

        # Calcul de l'étape suivante
        prochaine_etape = _etape_suivante(conge)
        conge.etape_validation = prochaine_etape
        conge.validated_by = validated_by_login

        if prochaine_etape == 'termine':
            statut_approuve = Statut.objects.get(code='approuve')
            conge.statut = statut_approuve

        conge.save()

        # Envoyer la notification pour la nouvelle étape
        envoi_notification_suivante(conge)

        return conge

    @staticmethod
    def refuser_etape(conge_id: int, validated_by_login) -> Conge:
        """
        Refuse le congé à n'importe quelle étape.
        Notifie le demandeur.
        """
        from api.signal.conge_signal import envoi_notification_refus

        conge = Conge.objects.get(id=conge_id)
        statut_refuse = Statut.objects.get(code='refuse')

        conge.statut = statut_refuse
        conge.etape_validation = 'termine'  # Fin du circuit
        conge.validated_by = validated_by_login
        conge.save()

        envoi_notification_refus(conge, validated_by_login)
        return conge

    @staticmethod
    def accepterPassation(conge_id: int, validated_by_login) -> Conge:
        """
        Le remplaçant accepte la passation → on passe à l'étape 'chef'.
        """
        from api.signal.conge_signal import envoi_notification_suivante

        conge = Conge.objects.get(id=conge_id)
        conge.etape_validation = 'chef'
        conge.validated_by = validated_by_login
        conge.save()

        envoi_notification_suivante(conge)
        return conge

    @staticmethod
    def refuserPassation(conge_id: int, validated_by_login) -> Conge:
        """
        Le remplaçant refuse la passation → congé annulé.
        """
        conge = Conge.objects.get(id=conge_id)
        statut_annule = Statut.objects.get(code='annule')
        conge.statut = statut_annule
        conge.etape_validation = 'termine'
        conge.validated_by = validated_by_login
        conge.save()
        return conge

    @staticmethod
    def cancel(conge_id: int) -> Conge:
        conge = Conge.objects.get(id=conge_id)
        statut_annule = Statut.objects.get(code='annule')
        conge.statut = statut_annule
        conge.save()
=======
from api.models.conge.conge import Conge
from api.models.conge.statut import Statut
from django.utils import timezone

class CongeServices:
    
    @staticmethod
    def getAll():
        """Récupérer toutes les demandes de congé"""
        return Conge.objects.all().order_by("-created_at")

    @staticmethod
    def getById(id: int) -> Conge:
        """Récupérer une demande par son ID"""
        return Conge.objects.get(id=id)

    @staticmethod
    def getByPersonnel(personnel_id: int):
        """Récupérer toutes les demandes d'un employé"""
        return Conge.objects.filter(personnel_id=personnel_id).order_by("-created_at")

    @staticmethod
    def getEnAttente():
        """Récupérer uniquement les demandes en attente"""
        return Conge.objects.filter(statut__code='en_attente').order_by("-created_at")

    @staticmethod
    def create(data) -> Conge:
        """Créer une nouvelle demande de congé"""
        statut_en_attente = Statut.objects.get(id=1)

        conge = Conge.objects.create(
            personnel=data.get('personnel'),
            type_conge=data.get('type_conge'),
            solde_conge=data.get('solde_conge'),
            date_debut=data.get('date_debut'),
            date_fin=data.get('date_fin'),
            description=data.get('description'),
            passation_service=data.get('passation_service'),
            statut=statut_en_attente,
        )
        return conge

    @staticmethod
    def update(id: int, data) -> Conge:
        """Mettre à jour une demande de congé"""
        conge = Conge.objects.get(id=id)

        for field, value in data.items():
            if value is not None and hasattr(conge, field):
                setattr(conge, field, value)

        conge.save()
        return conge

    @staticmethod
    def delete(id: int) -> bool:
        """Supprimer une demande de congé"""
        conge = Conge.objects.get(id=id)
        conge.delete()
        return True

    @staticmethod
    def approve(conge_id: int, validated_by) -> Conge:
        """Valider (Approuver) une demande"""
        conge = Conge.objects.get(id=conge_id)
        statut_approuve = Statut.objects.get(code='approuve')
        
        conge.statut = statut_approuve
        conge.validated_by = validated_by
        conge.save()
        return conge

    @staticmethod
    def refuse(conge_id: int, validated_by) -> Conge:
        """Refuser une demande"""
        conge = Conge.objects.get(id=conge_id)
        statut_refuse = Statut.objects.get(code='refuse')
        
        conge.statut = statut_refuse
        conge.validated_by = validated_by
        conge.save()
        return conge

    @staticmethod
    def cancel(conge_id: int) -> Conge:
        """Annuler une demande"""
        conge = Conge.objects.get(id=conge_id)
        statut_annule = Statut.objects.get(code='annule')
        
        conge.statut = statut_annule
        conge.save()
>>>>>>> 23088e43 (mon enregistrement local)
        return conge