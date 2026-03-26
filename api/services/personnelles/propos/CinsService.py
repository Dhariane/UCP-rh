from api.models.propos.Cins import Cins
from api.dto.personnelles.propos.CinsDto import CinsDTO

class CinsService:

    @staticmethod
    def getAll():
        return Cins.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> Cins:
        return Cins.objects.get(id=id)

    @staticmethod
    def create(data) -> Cins:
        return Cins.objects.create(
            numeroCin=data.get("numeroCin"),
            dateCin=data.get("dateCin"),
            lieuCin=data.get("lieuCin"),
            numeroDuplicata=data.get("numeroDuplicata"),
            dateDuplicata=data.get("dateDuplicata"),
            lieuDuplicata=data.get("lieuDuplicata"),
            personnelle=data.get("personnelle")
        )

    @staticmethod
    def update(id: int, data: dict) -> Cins:
        """
        Met à jour dynamiquement les informations de la CIN.
        """
        cins = Cins.objects.get(id=id)
        
        for field, value in data.items():
            if hasattr(cins, field):
                setattr(cins, field, value)
        
        cins.save()
        return cins

    @staticmethod
    def getByIdDto(id: int) -> CinsDTO:
        cins = CinsService.getById(id)
        return CinsDTO(cins)

    @staticmethod
    def getAllDto():
        # Optionnel : Ajout de la récupération de la liste complète en DTO 
        # pour rester cohérent avec ProposService
        cins_list = CinsService.getAll()
        return CinsDTO(cins_list, many=True)