from api.models.banque.coordonneesBancaires import CoordonneesBancaires
import base64
from django.core.files.base import ContentFile
class CoordonneesBancaireServices:

    @staticmethod
    def getAll():
        return CoordonneesBancaires.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> CoordonneesBancaires:
        return CoordonneesBancaires.objects.get(id=id)

    @staticmethod
    def create(data) -> CoordonneesBancaires:
        # On donne directement le fichier au champ photoRib du modèle
        return CoordonneesBancaires.objects.create(
            rib=data.get('rib'),
            banque=data.get('banque'),
            agence=data.get('agence'),
            photoRib=data.get('photo_rib') # L'objet fichier direct
        )
    @staticmethod
    def update(id: int, data) -> CoordonneesBancaires:
        instance = CoordonneesBancaires.objects.get(id=id)
        
        # Mise à jour dynamique des champs fournis
        for field, value in data.items():
            setattr(instance, field, value)
            
        instance.save()
        return instance