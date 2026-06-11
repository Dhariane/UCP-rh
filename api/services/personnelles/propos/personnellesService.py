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
<<<<<<< HEAD
    def generate_matricule() -> str:
        """Génère un matricule au format séquentiel : 001/UCP"""
        # 1. Compter combien de personnels existent déjà en base
        total_personnels = Personnelles.objects.count()
        
        # 2. Le nouveau numéro sera le total + 1
        nouveau_numero = total_personnels + 1
        
        # 3. Formater sur 3 chiffres avec le suffixe /UCP (ex: 1 -> "001/UCP")
        return f"{nouveau_numero:03d}/UCP"

    @staticmethod
=======
>>>>>>> 23088e43 (mon enregistrement local)
    def create(data) -> Personnelles:

        file_photo = data.get("photoResidence")
        file_casier = data.get("casierjudiciaire")
        file_acte = data.get("acteNaissance")
        file_cin = data.get("cinphoto")
<<<<<<< HEAD
        matricule_genere = data.get("matricule") or PersonnelleServices.generate_matricule()
        return Personnelles.objects.create(
            matricule=matricule_genere,
=======
        return Personnelles.objects.create(
>>>>>>> 23088e43 (mon enregistrement local)
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