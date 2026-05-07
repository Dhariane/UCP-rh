from api.models.propos.etatCivils import EtatCivil
from api.dto import EtatCivilDTO
class EtatCivilService:

    @staticmethod
    def create(nom: str) -> EtatCivil:
        return EtatCivil.objects.create(nom=nom)

    @staticmethod
    def getAll():
        return EtatCivil.objects.all().order_by("id")

    @staticmethod
    def get(id):
        return EtatCivil.objects.get(id=id)
    @staticmethod
    def getById(id: int) -> EtatCivil:
        return EtatCivil.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom: str) -> EtatCivil:
        etatCivil = EtatCivil.objects.get(id=id)
        etatCivil.nom = nom
        etatCivil.save()
        return etatCivil

    @staticmethod
    def getByIdDto(id: int) -> EtatCivilDTO:
        etatCivil = EtatCivilService.getById(id)
        return EtatCivilDTO(etatCivil)
    @staticmethod
    def getAllDto():
        etatCivils = EtatCivilService.getAll()
        return EtatCivilDTO(etatCivils, many=True)
    