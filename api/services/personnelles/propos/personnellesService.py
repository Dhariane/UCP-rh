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
            quartier=data.get('quartier'),
            ville=data.get('ville'),
            telPerso=data.get("telPerso"),
            sexe=data.get('sexe'),
            adresse=data.get('adresse'), 
            photoResidence=file_photo,
            casierjudiciaire=file_casier,
            acteNaissance=file_acte,
            cinphoto=file_cin
        )

    @staticmethod
    def update(id: int, data) -> Personnelles:
        personne = Personnelles.objects.get(id=id)

        for field, value in data.items():
            # 🔥 sécurité importante
            if value is not None and hasattr(personne, field):
                setattr(personne, field, value)

        personne.save()
        return personne