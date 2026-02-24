from api.models.fonction.fonctions import Fonctions
from api.dto.personnelles.fonction.fonctionDto import FonctionDto

class FonctionService:

    @staticmethod
    def create(data) -> Fonctions:
        """
        Crée un objet Fonction de manière sécurisée.
        data doit être un dict avec les clés :
        - nom, dateDebut, dateFin, personnelle, service, poste, superieur
        - financement est optionnel
        """
        # Assurer que data est un dict (au cas où on reçoit du JSON en string)
        if isinstance(data, str):
            import json
            data = json.loads(data)

        # Créer la fonction en sécurisant les clés optionnelles
        return Fonctions.objects.create(
            nom=data.get('nom'),
            dateDebut=data.get('dateDebut'),
            dateFin=data.get('dateFin'),
            financement=data.get('financement'),  # optionnel, peut être None
            personnelle=data.get('personnelle'),
            service=data.get('service'),
            poste=data.get('poste'),
            superieur=data.get('superieur')
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
    def update(id: int, dateDebut=None, dateFin=None, personnelle=None, service=None, poste=None, superieur=None, financement=None) -> Fonctions:   
        fonction = Fonctions.objects.get(id=id)
        if dateDebut is not None:
            fonction.dateDebut = dateDebut
        if dateFin is not None:
            fonction.dateFin = dateFin
        if personnelle is not None:
            fonction.personnelle = personnelle
        if service is not None:
            fonction.service = service
        if poste is not None:
            fonction.poste = poste
        if superieur is not None:
            fonction.superieur = superieur
        if financement is not None:
            fonction.financement = financement
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