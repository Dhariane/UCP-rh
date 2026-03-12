from api.models.propos.propos import Propos
from api.dto import ProposDTO

class ProposService:

    @staticmethod
    def getAll():
        return Propos.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> Propos:
        return Propos.objects.get(id=id)

    @staticmethod
    def create(data) -> Propos:
        return Propos.objects.create(
            nif=data.get("nif"),
            stat=data.get("stat"),
            numeroCnaps=data.get("numeroCnaps"),
            tel=data.get("tel"),
            email=data.get("email"),              
            nombreEnfant=data.get("nombreEnfant"),
            etatCivil=data.get("etatCivil"),
            personnelle=data.get("personnelle")
        )

    @staticmethod
    def update(id: int, data: dict) -> Propos:
        """
        Met à jour une instance existante de Propos.
        Utilise setattr pour une mise à jour dynamique des champs fournis.
        """
        propos = Propos.objects.get(id=id)
        
        # On boucle sur les données pour mettre à jour les champs présents
        for field, value in data.items():
            if hasattr(propos, field):
                setattr(propos, field, value)
            
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