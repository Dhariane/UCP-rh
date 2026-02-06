
from api.models.banque.coordonneesBancaires import CoordonneesBancaires
from api.dto.personnelles.banque.coordonneBancaireDto import CoordonneesBancairesDto


class CoordonneesBancaireServices:
    @staticmethod
    def create(rib, banque, agence):
        coordonnees_bancaires = CoordonneesBancaires.objects.create(
            rib=rib,
            banque=banque,
            agence=agence
        )
        return CoordonneesBancairesDto(coordonnees_bancaires).data
    @staticmethod
    def getAll():
        return CoordonneesBancaires.objects.all().order_by("id")
    @staticmethod
    def getById(id: int) -> CoordonneesBancaires:
        return CoordonneesBancaires.objects.get(id=id)
    @staticmethod
    def update(id: int, rib, banque, agence) -> CoordonneesBancaires:
        coordonnees_bancaires = CoordonneesBancaires.objects.get(id=id)
        coordonnees_bancaires.rib = rib
        coordonnees_bancaires.banque = banque
        coordonnees_bancaires.agence = agence
        coordonnees_bancaires.save()
        return CoordonneesBancairesDto(coordonnees_bancaires).data
    @staticmethod
    def getByIdDto(id: int) -> CoordonneesBancairesDto:
        coordonnees_bancaires = CoordonneesBancaireServices.getById(id)    
        return CoordonneesBancairesDto(coordonnees_bancaires)
    @staticmethod
    def getAllDto():    
        coordonnees_bancaires = CoordonneesBancaireServices.getAll()
        return CoordonneesBancairesDto(coordonnees_bancaires, many=True)
    