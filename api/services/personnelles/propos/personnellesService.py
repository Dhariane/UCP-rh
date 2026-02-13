from api.models.propos.personnelles import Personnelles
from api.dto.personnelles.propos.proposDto import ProposDTO 
from api.models.propos.sexe import  Sexes

class PersonnellesService:

    @staticmethod
    def create(data) -> Personnelles:
        return Personnelles.objects.create(
            nom=data['nom'],
            prenom=data["prenom"],
            dateNaissance=data["dateNaissance"],
            lieuNaissance=data["lieuNaissance"],
            sexe=data["sexe"],
            propos=data["propos"],
            cin=data["cin"]
        )
    
    @staticmethod
    def get(id):
        return Personnelles.objects.get(id=id)
    @staticmethod
    def getAll():
        return Personnelles.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> Personnelles:
        return Personnelles.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom: str) -> Personnelles:
        personnelles = Personnelles.objects.get(id=id)
        personnelles.nom = nom
        personnelles.save()
        return personnelles

    @staticmethod
    def getByIdDto(id: int) -> ProposDTO:
        personnelles = PersonnellesService.getById(id)
        return ProposDTO(personnelles)
    @staticmethod
    def getAllDto():
        personnelles = PersonnellesService.getAll()
        return ProposDTO(personnelles, many=True)