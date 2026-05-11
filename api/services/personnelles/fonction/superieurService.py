from api.models.fonction.fonctions import Fonctions
from api.models.auth.login.loginModel import Login

class SuperieurService:

    @staticmethod
    def getAll():
        """Retourne tous les personnels avec leurs supérieurs"""
        fonctions = Fonctions.objects.select_related(
            'personnelle', 'service'
        ).prefetch_related(
            'superieurs__personnelle'
        ).filter(dateFin__isnull=True)
        return fonctions

    @staticmethod
    def update(fonction_id: int, superieurs_ids: list):
        """Mettre à jour les supérieurs d'une fonction"""
        fonction = Fonctions.objects.get(id=fonction_id)
        logins   = Login.objects.filter(id__in=superieurs_ids)
        fonction.superieurs.set(logins)
        return fonction