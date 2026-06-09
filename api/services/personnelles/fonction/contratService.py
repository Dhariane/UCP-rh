from api.models.fonction.contrat import Contrat
from api.dto.personnelles.fonction.contratDto import ContratDto
from django.db import transaction
from datetime import date, timedelta

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
            financement=data.get('financement'),
            is_actif=data.get('is_actif', True) # Prend en compte le nouveau champ
        )

    # --- TES AUTRES MÉTHODES ATTUELLES RESTENT INCHANGÉES ---
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


    # =========================================================================
    # LA NOUVELLE MÉTHODE POUR GERER L'ARCHIVAGE ET LE CHANGEMENT DE FINANCEMENT
    # =========================================================================
    @staticmethod
    @transaction.atomic # Sécurité : Si un truc plante, rien n'est modifié en base
    def changer_statut_carriere(personnelle_id, nouvelles_data) -> Contrat:
        """
        Clôture le contrat actif actuel et crée un nouveau contrat (avenant)
        contenant le nouveau financement, salaire, service ou fonction.
        """
        aujourdhui = date.today()
        hier = aujourdhui - timedelta(days=1)

        # 1. Trouver le contrat actuellement actif pour cet employé
        contrat_actuel = Contrat.objects.filter(
            personnelle_id=personnelle_id, 
            is_actif=True
        ).first()

        if contrat_actuel:
            # On clôture l'ancien contrat
            contrat_actuel.is_actif = False
            # Si le contrat n'avait pas de date de fin, on met la veille de la transition
            if not contrat_actuel.dateFin:
                contrat_actuel.dateFin = hier
            contrat_actuel.save()

        # 2. Préparer les données pour le NOUVEAU contrat archiviste
        # On récupère les valeurs de l'ancien contrat s'ils ne changent pas
        donnees_nouveau_contrat = {
            'NumeroContrat': nouvelles_data.get('NumeroContrat', f"{contrat_actuel.NumeroContrat if contrat_actuel else 'CT'}-REV-{aujourdhui.strftime('%Y%m%d')}"),
            'photoContrat': nouvelles_data.get('photoContrat', contrat_actuel.photoContrat if contrat_actuel else None),
            'typeContrat': nouvelles_data.get('typeContrat', contrat_actuel.typeContrat if contrat_actuel else None),
            'periodeEssai': nouvelles_data.get('periodeEssai', contrat_actuel.periodeEssai if contrat_actuel else None),
            'dateFinEssai': nouvelles_data.get('dateFinEssai', contrat_actuel.dateFinEssai if contrat_actuel else None),
            'salaire': nouvelles_data.get('salaire', contrat_actuel.salaire if contrat_actuel else None),
            'personnelle': Contrat.objects.get(id=contrat_actuel.id).personnelle if contrat_actuel else nouvelles_data['personnelle'],
            'service': nouvelles_data.get('service', contrat_actuel.service if contrat_actuel else None),
            'fonction': nouvelles_data.get('fonction', contrat_actuel.fonction if contrat_actuel else None),
            
            # C'est ici qu'on applique le nouveau Financement envoyé par le front
            'financement': nouvelles_data.get('financement', contrat_actuel.financement if contrat_actuel else None),
            
            # Le nouveau contrat commence aujourd'hui et est marqué comme Actif
            'dateDebut': nouvelles_data.get('dateDebut', aujourdhui),
            'dateFin': nouvelles_data.get('dateFin', None),
            'is_actif': True
        }

        # 3. Création du nouveau contrat
        nouveau_contrat = Contrat.objects.create(**donnees_nouveau_contrat)
        return nouveau_contrat