from api.models.propos.personnelles import Personnelles
from api.dto.personnelles.propos.proposDto import ProposDTO 
from api.models.propos.sexe import  Sexes

class PersonnellesService:

    @staticmethod
    def create(personnelle_dto) -> Personnelles:
        sexe_instance = Sexes.objects.get(pk=personnelle_dto.data["sexe"])

        return Personnelles.objects.create(
            nom=personnelle_dto.data["nom"],
            prenom=personnelle_dto.data["prenom"],
            dateNaissance=personnelle_dto.data["dateNaissance"],
            lieuNaissance=personnelle_dto.data["lieuNaissance"],
            sexe=sexe_instance
        )
    

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