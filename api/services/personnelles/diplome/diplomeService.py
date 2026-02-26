from api.models import Diplome
import base64
from django.core.files.base import ContentFile
class DiplomeService:
    
    @staticmethod
    def create(data) -> Diplome:
        return Diplome.objects.create(
            nom=data.get("nom"),
            etablissement=data.get("etablissement"),
            dateObtention=data.get("dateObtention"),
            photo=data.get("photo"), # C'est l'objet fichier direct
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