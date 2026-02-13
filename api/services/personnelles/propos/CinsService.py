from api.models.propos.Cins import Cins
from api.dto.personnelles.propos.CinsDto import CinsDTO

class CinsService:

    @staticmethod
    def create(data):
        return Cins.objects.create(
            numeroCin=data["numeroCin"],
            dateCin=data["dateCin"],
            lieuCin=data["lieuCin"]
        )
    @staticmethod
    def getAll():
        return Cins.objects.all().order_by("id")
    
    @staticmethod
    def getById(id: int) -> Cins:
        return Cins.objects.get(id=id)
    
    @staticmethod
    def update(id: int, numeroCin: int, dateCin, lieuCin: str) -> CinsDTO:
        cins = Cins.objects.get(id=id)
        cins.numeroCin = numeroCin
        cins.dateCin = dateCin
        cins.lieuCin = lieuCin
        cins.save()
        return CinsDTO(cins)
    
    @staticmethod
    def getByIdDto(id: int):
        cins = CinsService.getById(id)
        return CinsDTO(cins)