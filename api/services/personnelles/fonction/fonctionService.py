from api.models.fonction.fonctions import Fonctions
from api.dto.personnelles.fonction.fonctionDto import FonctionDto
from api.models.conge.soldeConge import SoldeConge  # ✅ ajouter cet import
from django.utils import timezone    

class FonctionService:

    @staticmethod
    def create(data) -> Fonctions:
        if isinstance(data, str):
            import json
            data = json.loads(data)

        fonction = Fonctions.objects.create(
            nom=data['nom'],
            dateDebut=data['dateDebut'],
            dateFin=data['dateFin'],
            financement=data['financement'],
            personnelle=data['personnelle'],
            service=data['service'],
            poste=data['poste'],
        )

        # ✅ Créer automatiquement le solde congé pour ce personnel
        SoldeConge.objects.get_or_create(
            personnel=fonction.personnelle,
            annee=timezone.now().year,
            defaults={'is_manual': False, 'utilise': 0}
        )

        return fonction

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