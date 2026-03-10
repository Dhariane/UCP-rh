from api.models.propos.personnelles import Personnelles
import base64
from django.core.files.base import ContentFile
class PersonnelleServices:
    
    @staticmethod
    def getAll():
        return Personnelles.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> Personnelles:
        return Personnelles.objects.get(id=id)

    @staticmethod
    def create(data) -> Personnelles:

        file_photo = data.get("photoResidence")
        file_casier = data.get("casierjudiciaire")
        file_acte = data.get("acteNaissance")
        file_cin = data.get("cinphoto")
        return Personnelles.objects.create(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            dateNaissance=data.get('dateNaissance'),
            lieuNaissance=data.get('lieuNaissance'),
            emailPerso=data.get('emailPerso'),
            telPerso=data.get("telPerso"),
            sexe=data.get('sexe'),
            propos=data.get('propos'),
            cin=data.get('cin'),
            adresse=data.get('adresse'), 
            photoResidence=file_photo,
            casierjudiciaire=file_casier,
            acteNaissance=file_acte,
            cinphoto=file_cin
        )

    @staticmethod
    def update(id: int, data) -> Personnelles:
        """
        Met à jour une instance existante.
        Si photoResidence n'est pas fourni dans 'data', l'ancienne est conservée.
        """
        personne = Personnelles.objects.get(id=id)
        
        # On boucle sur les données validées pour mettre à jour les champs
        for field, value in data.items():
            setattr(personne, field, value)
            
        personne.save()
        return personne