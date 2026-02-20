from api.models.propos.propos import Propos
from api.dto import ProposDTO
class ProposService:

    @staticmethod
    def create(data) -> Propos:
        return Propos.objects.create(
            nif=data["nif"],
            stat=data["stat"],
            numeroCnaps=data["numeroCnaps"],
            tel=data["tel"],
            email=data["email"],              
            nombreEnfant=data["nombreEnfant"],
            etatCivil=data["etatCivil"]
        )

    @staticmethod
    def getAll():
        return Propos.objects.all().order_by("id")

    @staticmethod
    def get(id):
        return Propos.objects.get(id=id)
    @staticmethod
    def getById(id: int) -> Propos:
        return Propos.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom: str) -> Propos:
        propos = Propos.objects.get(id=id)
        propos.nom = nom
        propos.save()
        return propos

    @staticmethod
    def getByIdDto(id: int) -> ProposDTO:
        propos = ProposService.getById(id)
        return ProposDTO(propos)
    @staticmethod
    def getAllDto():
        propos = ProposService.getAll()
        return ProposDTO(propos, many=True)
    