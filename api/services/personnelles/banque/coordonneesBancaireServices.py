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
        # Gestion du Base64 pour photo_rib
        rib_photo_data = data.get("photo_rib")
        file_rib = None
        
        if rib_photo_data and isinstance(rib_photo_data, str) and ";base64," in rib_photo_data:
            format, imgstr = rib_photo_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f"rib_{data.get('rib')[:10]}.{ext}" # On utilise les 10 premiers car. du RIB
            file_rib = ContentFile(base64.b64decode(imgstr), name=file_name)
        elif rib_photo_data:
            file_rib = rib_photo_data

        return CoordonneesBancaires.objects.create(
            rib=data.get('rib'),
            banque=data.get('banque'),
            agence=data.get('agence'),
            photoRib=file_rib
        )
    @staticmethod
    def update(id: int, data) -> CoordonneesBancaires:
        instance = CoordonneesBancaires.objects.get(id=id)
        
        # Mise à jour dynamique des champs fournis
        for field, value in data.items():
            setattr(instance, field, value)
            
        instance.save()
        return instance