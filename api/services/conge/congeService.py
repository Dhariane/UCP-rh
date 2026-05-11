from api.models.conge.conge import Conge
from api.models.conge.statut import Statut
from django.utils import timezone

class CongeServices:
    
    @staticmethod
    def getAll():
        """Récupérer toutes les demandes de congé"""
        return Conge.objects.all().order_by("-created_at")

    @staticmethod
    def getById(id: int) -> Conge:
        """Récupérer une demande par son ID"""
        return Conge.objects.get(id=id)

    @staticmethod
    def getByPersonnel(personnel_id: int):
        """Récupérer toutes les demandes d'un employé"""
        return Conge.objects.filter(personnel_id=personnel_id).order_by("-created_at")

    @staticmethod
    def getEnAttente():
        """Récupérer uniquement les demandes en attente"""
        return Conge.objects.filter(statut__code='en_attente').order_by("-created_at")

    @staticmethod
    def create(data) -> Conge:
        statut_attente = Statut.objects.get(id=1)  # ← attente_chef

        conge = Conge.objects.create(
            personnel         = data.get('personnel'),
            type_conge        = data.get('type_conge'),
            solde_conge       = data.get('solde_conge'),
            date_debut        = data.get('date_debut'),
            date_fin          = data.get('date_fin'),
            description       = data.get('description'),
            passation_service = data.get('passation_service'),
            statut            = statut_attente,
        )
        return conge

    @staticmethod
    def update(id: int, data) -> Conge:
        """Mettre à jour une demande de congé"""
        conge = Conge.objects.get(id=id)

        for field, value in data.items():
            if value is not None and hasattr(conge, field):
                setattr(conge, field, value)

        conge.save()
        return conge

    @staticmethod
    def delete(id: int) -> bool:
        """Supprimer une demande de congé"""
        conge = Conge.objects.get(id=id)
        conge.delete()
        return True

    @staticmethod
    def approve(conge_id: int, validated_by) -> Conge:
        """Valider (Approuver) une demande"""
        conge = Conge.objects.get(id=conge_id)
        statut_approuve = Statut.objects.get(code='approuve')
        
        conge.statut = statut_approuve
        conge.validated_by = validated_by
        conge.save()
        return conge

    @staticmethod
    def refuse(conge_id: int, validated_by) -> Conge:
        """Refuser une demande"""
        conge = Conge.objects.get(id=conge_id)
        statut_refuse = Statut.objects.get(code='refuse')
        
        conge.statut = statut_refuse
        conge.validated_by = validated_by
        conge.save()
        return conge

    @staticmethod
    def cancel(conge_id: int) -> Conge:
        """Annuler une demande"""
        conge = Conge.objects.get(id=conge_id)
        statut_annule = Statut.objects.get(code='annule')
        
        conge.statut = statut_annule
        conge.save()
        return conge