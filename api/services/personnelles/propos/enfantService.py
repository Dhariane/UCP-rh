from api.models import Enfant

class EnfantService:
    
    @staticmethod
    def create(data) -> Enfant:
        return Enfant.objects.create(
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            dateNaissance=data.get("dateNaissance"),
            lieuNaissance=data.get("lieuNaissance"),
            certificatVie=data.get("certificatVie"),
            personnelle_id=data.get("personnelle"),
            sexe_id=data.get("sexe")
        )

    @staticmethod
    def getAll():
        return Enfant.objects.all().order_by("nom")

    @staticmethod
    def getById(id: int) -> Enfant:
        return Enfant.objects.get(id=id)

    @staticmethod
    def update(id: int, data: dict) -> Enfant:
        enfant = Enfant.objects.get(id=id)
        for key, value in data.items():
            if hasattr(enfant, key) and value is not None:
                setattr(enfant, key, value)
        enfant.save()
        return enfant

    @staticmethod
    def delete(id: int):
        enfant = Enfant.objects.get(id=id)
        enfant.delete()
        return True