from api.models import Superieur
from api.dto.personnelles.fonction.superieurDto import SuperieurDto

class SuperieurService:
    @staticmethod
    def create(nom: str)-> Superieur:
        return Superieur.objects.create(nom=nom)

    @staticmethod
    def getAll()-> list[Superieur]:
        return Superieur.objects.all().order_by("id")

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
        return SuperieurDto(superieurs, many=True) 