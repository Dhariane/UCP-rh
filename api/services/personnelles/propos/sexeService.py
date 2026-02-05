from api.models.propos.sexe import Sexes 
from api.dto.personnelles.propos.sexeDto import SexeDTO   

class SexeService:
    @staticmethod
    def create(nom: str) -> Sexes:
        return Sexes.objects.create(nom=nom)
    
    @staticmethod
    def getAll():
        return Sexes.objects.all().order_by("id")    
    
    @staticmethod
    def getById(id: int) -> Sexes:
        return Sexes.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom: str) -> Sexes:
        sexe = Sexes.objects.get(id=id)
        sexe.nom = nom
        sexe.save()
        return sexe
    
    @staticmethod
    def getByIdDto(id: int) -> SexeDTO:
        sexe = SexeService.getById(id)
        return SexeDTO(sexe)
    
    @staticmethod
    def getAllDto():
        sexes = SexeService.getAll()
        return SexeDTO(sexes, many=True)
        