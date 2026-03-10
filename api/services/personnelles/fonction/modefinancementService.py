from api.models.fonction.modefinancement import ModeFinancement
# Importez votre DTO si vous en avez un pour ModeFinancement
# from api.dto.votre_chemin.ModeFinancementDto import ModeFinancementDTO
from api.dto.personnelles.fonction.modefinancementDto import ModefinancementDto
class ModeFinancementService:
    @staticmethod
    def create(data) -> ModeFinancement:
        return ModeFinancement.objects.create(
            nom=data['nom']
        )

    @staticmethod
    def getAll():
        return ModeFinancement.objects.all().order_by("id")
    
    @staticmethod
    def get(id: int) -> ModeFinancement:
        return ModeFinancement.objects.get(id=id)

    @staticmethod
    def getById(id: int) -> ModeFinancement:
        return ModeFinancement.objects.get(id=id)
    
    @staticmethod
    def update(id: int, nom: str) -> ModeFinancement:   
        mode = ModeFinancement.objects.get(id=id)
        mode.nom = nom
        mode.save()
        return mode
    
    @staticmethod
    def getByIdDto(id: int) -> ModefinancementDto:  
         mode = ModeFinancementService.getById(id)
         return ModefinancementDto(mode)
    
    @staticmethod
    def getAllDto():        
        mode = ModeFinancementService.getAll()
        return ModefinancementDto(mode, many=True)