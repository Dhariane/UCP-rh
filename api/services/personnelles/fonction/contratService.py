from api.models.fonction.contrat import Contrat
from api.dto.personnelles.fonction.contratDto import ContratDto

class ContratService:
    @staticmethod
    def create(data) -> Contrat:
        return Contrat.objects.create(
            NumeroContrat=data['NumeroContrat'],
            photoContrat=data.get('photoContrat'),
            typeContrat=data['typeContrat'],
            periodeEssai=data.get('periodeEssai'),
            dateFinEssai=data.get('dateFinEssai'),
            salaire=data['salaire'],
            personnelle=data['personnelle'],
            service=data['service'],
            fonction=data.get('fonction'),
            dateDebut=data.get('dateDebut'),
            dateFin=data.get('dateFin'),
            financement=data.get('financement')
        )

    @staticmethod
    def getAll():
        return Contrat.objects.all().order_by("id")

    @staticmethod
    def get(id):
        return Contrat.objects.get(id=id)

    @staticmethod
    def getById(id: int) -> Contrat:
        return Contrat.objects.get(id=id)

    @staticmethod
    def update(id: int, NumeroContrat=None, photoContrat=None, typeContrat=None, personnelle=None) -> Contrat:
        contrat = Contrat.objects.get(id=id)
        if NumeroContrat is not None:
            contrat.NumeroContrat = NumeroContrat
        if photoContrat is not None:
            contrat.photoContrat = photoContrat
        if typeContrat is not None:
            contrat.typeContrat = typeContrat
        if personnelle is not None:
            contrat.personnelle = personnelle
        contrat.save()
        return contrat

    @staticmethod
    def getByIdDto(id: int) -> ContratDto:
        contrat = ContratService.getById(id)
        return ContratDto(contrat)

    @staticmethod
    def getAllDto():
        contrats = ContratService.getAll()
        return ContratDto(contrats, many=True)
