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
    def update(id, data):
        try:
            Cins.objects.filter(id=id).update(**data)
            return Cins.objects.get(id=id)
        except Exception as e:
            print(f"Erreur Service CIN: {e}")
            raise e

    @staticmethod
    def getByIdDto(id: int) -> CinsDTO:
        cins = CinsService.getById(id)
        return CinsDTO(cins)

    @staticmethod
    def getAllDto():
        cins_list = CinsService.getAll()
        return CinsDTO(cins_list, many=True)