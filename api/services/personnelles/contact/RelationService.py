from api.models.contact.relation import Relations
from api.dto.personnelles.contact.RelationDto import RelationDto

class RelationService:

    @staticmethod
    def create(nom: str, grade: str) -> Relations:
        return Relations.objects.create(nom=nom, grade=grade)

    @staticmethod
    def getAll():
        return Relations.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> Relations:
        return Relations.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom: str, grade: str) -> Relations:
        relation = Relations.objects.get(id=id)
        relation.nom = nom
        relation.grade = grade
        relation.save()
        return relation

    @staticmethod
    def getByIdDto(id: int) -> RelationDto:
        relation = RelationService.getById(id)
        return RelationDto(relation)
    
    @staticmethod
    def getAllDto():
        relations = RelationService.getAll()
        return RelationDto(relations, many=True)