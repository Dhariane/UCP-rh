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
        # Gestion du Base64 pour photoResidence
        photo_data = data.get("photoResidence")
        file_photo = None
        
        if photo_data and isinstance(photo_data, str) and ";base64," in photo_data:
            format, imgstr = photo_data.split(';base64,')
            ext = format.split('/')[-1]
            # On utilise le nom de la personne pour nommer le fichier
            file_name = f"residence_{data.get('nom')}_{data.get('prenom')}.{ext}"
            file_photo = ContentFile(base64.b64decode(imgstr), name=file_name)
        elif photo_data:
            file_photo = photo_data

        return Personnelles.objects.create(
            nom=data.get('nom'),
            prenom=data.get('prenom'),
            dateNaissance=data.get('dateNaissance'),
            lieuNaissance=data.get('lieuNaissance'),
            sexe=data.get('sexe'),
            propos=data.get('propos'),
            cin=data.get('cin'),
            adresse=data.get('adresse'), # Champ adresse que vous avez ajouté
            photoResidence=file_photo
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