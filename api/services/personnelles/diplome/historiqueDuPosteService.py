from api.models import HistoriqueDuPoste

class HistoriqueDuPosteService:
    
    @staticmethod
    def create(data) -> HistoriqueDuPoste:
        return HistoriqueDuPoste.objects.create(
            poste=data.get("poste"),
            société=data.get("société"),
            datedebut=data.get("datedebut"),
            datefin=data.get("datefin"),
            description=data.get("description"),
            personnelle_id=data.get("personnelle")
        )

    @staticmethod
    def getAll():
        return HistoriqueDuPoste.objects.all().order_by("-datedebut")

    @staticmethod
    def getById(id: int) -> HistoriqueDuPoste:
        return HistoriqueDuPoste.objects.get(id=id)

    @staticmethod
    def update(id: int, data: dict) -> HistoriqueDuPoste:
        historique = HistoriqueDuPoste.objects.get(id=id)
        for key, value in data.items():
            if hasattr(historique, key):
                setattr(historique, key, value)
        historique.save()
        return historique

    @staticmethod
    def delete(id: int):
        historique = HistoriqueDuPoste.objects.get(id=id)
        historique.delete()
        return True