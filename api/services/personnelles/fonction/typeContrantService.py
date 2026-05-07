from api.models.fonction.typeContrat import TypeContrats
from api.dto.personnelles.fonction.typecontratDto import TypeContratDto

class TypeContratService:
    @staticmethod
    def create(data) -> TypeContrats:
        return TypeContrats.objects.create(
            TypeContrat=data['TypeContrat']
        )

    @staticmethod
    def getAll():
        return TypeContrats.objects.all().order_by("id")

    @staticmethod
    def get(id):
        return TypeContrats.objects.get(id=id)

    @staticmethod
    def getById(id: int) -> TypeContrats:
        return TypeContrats.objects.get(id=id)

    @staticmethod
    def update(id: int, TypeContrat: str) -> TypeContrats:
        t = TypeContrats.objects.get(id=id)
        t.TypeContrat = TypeContrat
        t.save()
        return t

    @staticmethod
    def getByIdDto(id: int) -> TypeContratDto:
        t = TypeContratService.getById(id)
        return TypeContratDto(t)

    @staticmethod
    def getAllDto():
        ts = TypeContratService.getAll()
        return TypeContratDto(ts, many=True)
