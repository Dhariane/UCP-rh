
from django.utils import timezone
from api.models.conge.passationservice import PassationService
from api.models.conge.conge import Conge


class PassationServices:

    # ─────────────────────────────────────────────
    # HELPER — vérification congé actif
    # ─────────────────────────────────────────────

    @staticmethod
    def _est_en_conge(personnel) -> bool:
        today = timezone.now().date()
        return Conge.objects.filter(
            personnel=personnel,
            statut_id=2,
            date_debut__lte=today,
            date_fin__gte=today
        ).exists()

    @staticmethod
    def _get_conge_actif(personnel):
        today = timezone.now().date()
        return Conge.objects.filter(
            personnel=personnel,
            statut_id=2,
            date_debut__lte=today,
            date_fin__gte=today
        ).select_related('type_conge').first()

    # ─────────────────────────────────────────────
    # CRUD
    # ─────────────────────────────────────────────

    @staticmethod
    def getAll():
        return PassationService.objects.select_related(
            'titulaire', 'statut', 'remplacant'
        ).all()

    @staticmethod
    def getById(id: int):
        return PassationService.objects.select_related(
            'titulaire', 'statut', 'remplacant'
        ).get(pk=id)

    @staticmethod
    def create(data: dict):
        """
        Crée une passation après avoir vérifié que :
        1. Le titulaire est bien en congé actif.
        2. Le remplaçant N'est PAS en congé au même moment.
        """
        titulaire  = data.get('titulaire')
        remplacant = data.get('remplacant')

        # ── 1. Le titulaire doit être en congé ──
        if titulaire and not PassationServices._est_en_conge(titulaire):
            raise ValueError(
                "Le titulaire n'a pas de congé approuvé en cours. "
                "Une passation de service n'est possible que pendant un congé actif."
            )

        # ── 2. Le remplaçant ne doit pas être en congé ──
        if remplacant:
            conge_remplacant = PassationServices._get_conge_actif(remplacant)
            if conge_remplacant:
                date_fin = conge_remplacant.date_fin.strftime('%d/%m/%Y')
                raise ValueError(
                    f"Le remplaçant désigné est actuellement en congé "
                    f"jusqu'au {date_fin}. "
                    f"Veuillez choisir un autre remplaçant disponible."
                )

        return PassationService.objects.create(**data)

    @staticmethod
    def update(id: int, data: dict):
        """
        Met à jour une passation.
        Si le remplaçant change, re-vérifie sa disponibilité.
        """
        passation = PassationService.objects.get(pk=id)

        nouveau_remplacant = data.get('remplacant')
        if nouveau_remplacant and nouveau_remplacant != passation.remplacant:
            conge_remplacant = PassationServices._get_conge_actif(nouveau_remplacant)
            if conge_remplacant:
                date_fin = conge_remplacant.date_fin.strftime('%d/%m/%Y')
                raise ValueError(
                    f"Le nouveau remplaçant est en congé jusqu'au {date_fin}. "
                    f"Veuillez choisir un remplaçant disponible."
                )

        for attr, value in data.items():
            setattr(passation, attr, value)
        passation.save()
        return passation

    @staticmethod
    def delete(id: int):
        passation = PassationService.objects.get(pk=id)
        passation.delete()

    # ─────────────────────────────────────────────
    # UTILITAIRE : vérifier la disponibilité
    # ─────────────────────────────────────────────

    @staticmethod
    def verifier_disponibilite(personnel_id: int) -> dict:
        """
        Vérifie si un personnel est disponible pour être remplaçant.
        Utilisé par le controller /passation/disponibilite/<id>/
        """
        from api.models.auth.login.loginModel import Login
        try:
            login = Login.objects.select_related('personnelle').get(pk=personnel_id)
            personnel = login.personnelle
        except Login.DoesNotExist:
            return {"disponible": False, "raison": "Personnel introuvable."}

        conge = PassationServices._get_conge_actif(personnel)
        if conge:
            return {
                "disponible": False,
                "raison": (
                    f"En congé du {conge.date_debut.strftime('%d/%m/%Y')} "
                    f"au {conge.date_fin.strftime('%d/%m/%Y')}."
                ),
                "date_debut": str(conge.date_debut),
                "date_fin":   str(conge.date_fin),
            }

        return {"disponible": True, "raison": "Disponible pour remplacement."}

