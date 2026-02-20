from api.models.propos.famille import Famille
from api.dto.personnelles.propos.familleDto import FamilleDto

class FamilleService:

    @staticmethod
    def create(data)-> Famille:
        return Famille.objects.create(
            nomPere=data["nomPere"],
            prenomPere=data["prenomPere"],
            nomMere=data["nomMere"],
            prenomMere=data["prenomMere"],
            nomConjoint=data["nomConjoint"],
            prenomConjoint=data["prenomConjoint"],
            nombreEnfant=data["nombreEnfant"],
            personnelle=data["personnelle"]
        )
    @staticmethod
    def getAll():
        return Famille.objects.all().order_by("id")
    
    @staticmethod
    def getById(id : int) -> Famille:
        return Famille.objects.get(id=id)
    
    @staticmethod
    def update(id: int, data: dict) -> Famille:
        # 1. On récupère l'instance existante
        Familles = Famille.objects.get(id=id)
        
        # 2. On boucle sur les clés envoyées dans le dictionnaire 'data'
        for key, value in data.items():
            # On vérifie que l'attribut existe bien dans le modèle pour éviter les erreurs
            if hasattr(Familles, key):
                setattr(Familles, key, value)
        
        # 3. On enregistre les modifications en une seule fois
        Familles.save()
        return Familles
    @staticmethod
    def getByIdDto(id:int) -> FamilleDto:
        Familles = FamilleService.getById(id)
        return FamilleDto(Familles)
    
    @staticmethod
    def getAllDto():
        Familles = FamilleService.getAll()
        return FamilleDto(Familles,many=True)