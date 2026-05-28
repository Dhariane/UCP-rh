from api.models.diplome.diplome import Diplome 
import base64
from django.core.files.base import ContentFile

class DiplomeService:
    
    @staticmethod
    def create(data):
        # Gestion de la photo (si elle est envoyée en base64)
        photo = data.get("photo")
        if photo and isinstance(photo, str) and photo.startswith("data:image"):
            format, imgstr = photo.split(';base64,')
            ext = format.split('/')[-1]
            photo = ContentFile(base64.b64decode(imgstr), name=f"diplome_{data.get('personnelle')}.{ext}")

        return Diplome.objects.create(
            type_diplome_id=data.get("type_diplome"),
            filiere=data.get("filiere"),
            etablissement=data.get("etablissement"),
            anneeObtention=data.get("anneeObtention"),
            lieu=data.get("lieu"),
            photo=photo,
            personnelle_id=data.get("personnelle")
        )

    @staticmethod
    def getAll():
        return Diplome.objects.all().select_related('type_diplome', 'personnelle').order_by("-anneeObtention")

    @staticmethod
    def getById(id: int):
        return Diplome.objects.select_related('type_diplome', 'personnelle').get(id=id)

    @staticmethod
    def update(id: int, data: dict):
        diplome = Diplome.objects.get(id=id)
        
        # Gestion photo si nouvelle photo envoyée
        if "photo" in data and data.get("photo") and isinstance(data.get("photo"), str) and data["photo"].startswith("data:image"):
            format, imgstr = data["photo"].split(';base64,')
            ext = format.split('/')[-1]
            diplome.photo = ContentFile(base64.b64decode(imgstr), name=f"diplome_{id}.{ext}")

        for key, value in data.items():
            if key == "photo":
                continue  # déjà géré
            if hasattr(diplome, key) and value is not None:
                if key == "type_diplome":
                    setattr(diplome, "type_diplome_id", value)
                else:
                    setattr(diplome, key, value)
        
        diplome.save()
        return diplome

    @staticmethod
    def delete(id: int):
        diplome = Diplome.objects.get(id=id)
        diplome.delete()
        return True