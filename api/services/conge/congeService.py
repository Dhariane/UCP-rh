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
        try:
            statut_attente = Statut.objects.get(id=1)
        except Statut.DoesNotExist:
            raise ValueError("Le statut initial (ID: 1) n'existe pas en base de données.")

        # On extrait proprement chaque champ validé par le DTO
        conge = Conge.objects.create(
            personnel=data.get('personnel'),
            type_conge=data.get('type_conge'),
            solde_conge=data.get('solde_conge'),
            date_debut=data.get('date_debut'),
            date_fin=data.get('date_fin'),
            description=data.get('description'),
            passation_service=data.get('passation_service'),  # L'instance ou None
            statut=statut_attente,
            validated_by=data.get('validated_by')
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
    
    @staticmethod
    def accepterPassation(conge_id: int) -> Conge:
        """
        Appelé quand le remplaçant accepte la passation de service.
        Fait passer directement le congé à l'étape du chef direct.
        """
        conge = Conge.objects.get(id=conge_id)
        
        # On fait passer l'étape au chef direct
        conge.etape_validation = 'chef'
        conge.save()
        
        # 🚨 On déclenche manuellement la notification vers le chef 
        # en important la fonction depuis ton fichier de signaux
        from api.signal.conge_signal import envoi_notification_suivante
        envoi_notification_suivante(conge)
        
        return conge