from api.models import Formation
import base64
from django.core.files.base import ContentFile
class FormationService:
    
    @staticmethod
    def create(data) -> Formation:
        attestation_data = data.get("attestation")
        file_attestation = None
        
        if attestation_data and isinstance(attestation_data, str) and "," in attestation_data:
            format, imgstr = attestation_data.split(';base64,')
            ext = format.split('/')[-1]
            file_attestation = ContentFile(base64.b64decode(imgstr), name=f"attestation_{data.get('titre')}.{ext}")
        elif attestation_data:
            file_attestation = attestation_data

        return Formation.objects.create(
            titre=data.get("titre"),
            organisme=data.get("organisme"),
            datedebut=data.get("datedebut"),
            datefin=data.get("datefin"),
            attestation=file_attestation,
            personnelle_id=data.get("personnelle")
        )

    @staticmethod
    def getAll():
        return Formation.objects.all().order_by("-datedebut")

    @staticmethod
    def getById(id: int) -> Formation:
        return Formation.objects.get(id=id)

    @staticmethod
    def update(id: int, data: dict) -> Formation:
        formation = Formation.objects.get(id=id)
        for key, value in data.items():
            if hasattr(formation, key) and value is not None:
                setattr(formation, key, value)
        formation.save()
        return formation

    @staticmethod
    def delete(id: int):
        formation = Formation.objects.get(id=id)
        formation.delete()
        return True