from api.models import Diplome
import base64
from django.core.files.base import ContentFile
class DiplomeService:
    
    @staticmethod
    def create(data) -> Diplome:
        photo_data = data.get("photo")
        file_photo = None
        
        # Si on reçoit une chaîne Base64
        if photo_data and isinstance(photo_data, str) and "," in photo_data:
            format, imgstr = photo_data.split(';base64,')
            ext = format.split('/')[-1]
            file_photo = ContentFile(base64.b64decode(imgstr), name=f"diplome_{data.get('nom')}.{ext}")
        elif photo_data: # Cas où c'est déjà un fichier ou une chaîne simple
            file_photo = photo_data

        return Diplome.objects.create(
            nom=data.get("nom"),
            etablissement=data.get("etablissement"),
            dateObtention=data.get("dateObtention"),
            photo=file_photo, # On passe le fichier décodé
            personnelle_id=data.get("personnelle")
        )

    @staticmethod
    def getAll():
        return Diplome.objects.all().order_by("-dateObtention")

    @staticmethod
    def getById(id: int) -> Diplome:
        return Diplome.objects.get(id=id)

    @staticmethod
    def update(id: int, data: dict) -> Diplome:
        diplome = Diplome.objects.get(id=id)
        for key, value in data.items():
            if hasattr(diplome, key) and value is not None:
                setattr(diplome, key, value)
        diplome.save()
        return diplome

    @staticmethod
    def delete(id: int):
        diplome = Diplome.objects.get(id=id)
        diplome.delete()
        return True