from api.models.banque.banques import Banques
from api.dto.personnelles.banque.banqueDto import BanqueDto

class BanqueService:  
    @staticmethod
    def create(data) -> Banques:
        return Banques.objects.create(nom=data['nom'])

    @staticmethod
    def getAll():
        return Banques.objects.all().order_by("id")
    
    @staticmethod
    def get(id):
        return Banques.objects.get(id=id)
    @staticmethod
    def getById(id: int) -> Banques:
        return Banques.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom) -> Banques:   
        banque = Banques.objects.get(id=id)
        banque.nom = nom
        banque.save()
        return banque
    
    @staticmethod
    def getByIdDto(id: int) -> BanqueDto:  
        banque = BanqueService.getById(id)
        return BanqueDto(banque)  
    
    @staticmethod
    def getAllDto():        
        banques = BanqueService.getAll()
        return BanqueDto(banques, many=True)