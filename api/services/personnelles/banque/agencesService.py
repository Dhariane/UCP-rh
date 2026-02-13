
from api.dto.personnelles.banque.agencesDto import AgenceDto
from api.models.banque.agences import Agences

class AgenceService:
    @staticmethod
    def create(data) -> Agences:
        if isinstance(data, str):
            data = {"nom": data}

        return Agences.objects.create(nom=data["nom"])


    @staticmethod
    def getAll():
        return Agences.objects.all().order_by("id")
    
    @staticmethod
    def get(id):
        return AgenceService.objects.get(id=id)
    @staticmethod
    def getById(id: int) -> Agences:
        return Agences.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom) -> Agences:   
        agence = Agences.objects.get(id=id)
        agence.nom = nom
        agence.save()
        return agence
    
    @staticmethod
    def getByIdDto(id: int) -> AgenceDto:  
        agence = AgenceService.getById(id)
        return AgenceDto(agence)  
    
    @staticmethod
    def getAllDto():        
        agences = AgenceService.getAll()
        return AgenceDto(agences, many=True)