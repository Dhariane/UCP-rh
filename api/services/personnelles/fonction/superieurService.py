<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> dcc45aed (linux)
from api.models import Superieur
from api.dto.personnelles.fonction.superieurDto import SuperieurDto

class SuperieurService:
    @staticmethod
    def create(data)-> Superieur:
        return Superieur.objects.create(nom=data['nom'])

    @staticmethod
    def getAll()-> list[Superieur]:
        return Superieur.objects.all().order_by("id")
    @staticmethod
    def get(id):
        return Superieur.objects.get(id=id)
    @staticmethod
    def getById(id: int)-> Superieur:
        return Superieur.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom: str)-> Superieur:
        superieur = Superieur.objects.get(id=id)
        superieur.nom = nom
        superieur.save()
        return superieur
    @staticmethod
    def getByIdDto(id: int)-> SuperieurDto:
        superieur = SuperieurService.getById(id)
        return SuperieurDto(superieur)
    
    @staticmethod
    def getAllDto()-> list[SuperieurDto]:
        
        superieurs = SuperieurService.getAll()
<<<<<<< HEAD
        return SuperieurDto(superieurs, many=True) 
=======
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
>>>>>>> cb65f867728df1dc0fb2754ea892270f8c03e70e
=======
        return SuperieurDto(superieurs, many=True) 
>>>>>>> dcc45aed (linux)
