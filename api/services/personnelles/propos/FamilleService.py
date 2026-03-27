from api.models.propos.famille import Famille
from api.dto.personnelles.propos.familleDto import FamilleDto

class FamilleService:

    @staticmethod
    def create(data)-> Famille:
        return Famille.objects.create(
            nomPere=data.get("nomPere"),
            nomMere=data.get("nomMere"),
            nomConjoint=data.get("nomConjoint"),
            prenomConjoint=data.get("prenomConjoint"),
            telConjoint=data.get("telConjoint"),
            adresseConjoint=data.get("adresseConjoint"),
            emailConjoint=data.get("emailConjoint"),
            nombreEnfant=data.get("nombreEnfant"),
            acteMariage=data.get("acteMariage"),
            personnelle=data.get("personnelle")
        )
    @staticmethod
    def getAll():
        return Famille.objects.all().order_by("id")
    
    @staticmethod
    def getById(id : int) -> Famille:
        return Famille.objects.get(id=id)
    
    @staticmethod
    def update(id: int, data: dict) -> Famille:
        # On récupère l'instance
        instance = Famille.objects.get(id=id)
        
        # On met à jour uniquement les champs envoyés dans 'data'
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        
        instance.save()
        return instance
    @staticmethod
    def getByIdDto(id:int) -> FamilleDto:
        Familles = FamilleService.getById(id)
        return FamilleDto(Familles)
    
    @staticmethod
    def getAllDto():
        Familles = FamilleService.getAll()
        return FamilleDto(Familles,many=True)