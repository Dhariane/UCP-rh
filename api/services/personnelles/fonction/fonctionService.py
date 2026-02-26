from api.models.fonction.fonctions import Fonctions
from api.dto.personnelles.fonction.fonctionDto import FonctionDto

class FonctionService:  
    @staticmethod
    def create(data) -> Fonctions:
        return Fonctions.objects.create(
            nom=data['nom'],
            dateDebut=data['dateDebut'],
            dateFin=data['dateFin'],
            financement=data['financement'],
            personnelle=data['personnelle'],
            service=data['service'],
            poste=data['poste'],
            superieur=data['superieur']
        )

    @staticmethod
    def getAll():
        return Fonctions.objects.all().order_by("id")
    @staticmethod
    def get(id):
        return Fonctions.objects.get(id=id)
    @staticmethod
    def getById(id: int) -> Fonctions:
        return Fonctions.objects.get(id=id)
    
    @staticmethod
    def update(id: int, dateDebut, dateFin, personnelle, service, poste) -> Fonctions:   
        fonction = Fonctions.objects.get(id=id)
        fonction.dateDebut = dateDebut
        fonction.dateFin = dateFin
        fonction.personnelle = personnelle
        fonction.service = service
        fonction.poste = poste
        fonction.save()
        return fonction
    
    @staticmethod
    def getByIdDto(id: int) -> FonctionDto:  
        fonction = FonctionService.getById(id)
        return FonctionDto(fonction)  
    
    @staticmethod
    def getAllDto():        
        fonctions = FonctionService.getAll()
        return FonctionDto(fonctions, many=True)