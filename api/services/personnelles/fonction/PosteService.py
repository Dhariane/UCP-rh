from api.models.fonction.poste import Postes
from api.dto.personnelles.fonction.PosteDto import PosteDTO

class PosteService:
    @staticmethod
    def create(nom: str, grade: str) -> Postes:
        return Postes.objects.create(nom=nom, grade=grade)

    @staticmethod
    def getAll():
        return Postes.objects.all().order_by("id")
    
    @staticmethod
    def getById(id: int) -> Postes:
        return Postes.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom: str, grade: str) -> Postes:   
        poste = Postes.objects.get(id=id)
        poste.nom = nom
        poste.grade = grade
        poste.save()
        return poste
    
    @staticmethod
    def getByIdDto(id: int) -> PosteDTO:  
        poste = PosteService.getById(id)
        return PosteDTO(poste)
