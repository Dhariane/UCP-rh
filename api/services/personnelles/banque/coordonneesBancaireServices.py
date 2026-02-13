
from api.models.banque.coordonneesBancaires import CoordonneesBancaires
from api.dto.personnelles.banque.coordonneBancaireDto import CoordonneesBancairesDto
from api.models.banque.agences import Agences
from api.models.banque.banques import Banques

class CoordonneesBancaireServices:
    @staticmethod
    def create(data) -> CoordonneesBancaires:
        return CoordonneesBancaires.objects.create(
            agence=data['agence'],
            banque=data['banque'],
            rib=data['rib']
        )

    @staticmethod
    def getAll():
        return CoordonneesBancaires.objects.all().order_by("id")
    @staticmethod
    def get(id):
        return CoordonneesBancaires.objects.get(id=id)
    @staticmethod
    def getById(id: int) -> CoordonneesBancaires:
        return CoordonneesBancaires.objects.get(id=id)
    @staticmethod
    def update(id: int, rib, banque, agence) -> CoordonneesBancaires:
        coordonnees_bancaires = CoordonneesBancaires.objects.get(id=id)
        coordonnees_bancaires.banque = banque
        coordonnees_bancaires.agence = agence
        coordonnees_bancaires.rib = rib
        coordonnees_bancaires.save()
        return CoordonneesBancairesDto(coordonnees_bancaires)
    @staticmethod
    def getByIdDto(id: int) -> CoordonneesBancairesDto:
        coordonnees_bancaires = CoordonneesBancaireServices.getById(id)    
        return CoordonneesBancairesDto(coordonnees_bancaires)
    @staticmethod
    def getAllDto():    
        coordonnees_bancaires = CoordonneesBancaireServices.getAll()
        return CoordonneesBancairesDto(coordonnees_bancaires, many=True)
    