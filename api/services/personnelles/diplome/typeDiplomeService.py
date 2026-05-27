from api.models.diplome.typeDiplome import DiplomeType

class DiplomeTypeService:
    
    @staticmethod
    def create(data):
        return DiplomeType.objects.create(
            nom=data.get("nom"),
        )

    @staticmethod
    def getAll():
        return DiplomeType.objects.all().order_by("nom")

    @staticmethod
    def getById(id: int):
        return DiplomeType.objects.get(id=id)

    @staticmethod
    def update(id: int, data: dict):
        diplome_type = DiplomeType.objects.get(id=id)
        for key, value in data.items():
            if hasattr(diplome_type, key) and value is not None:
                setattr(diplome_type, key, value)
        diplome_type.save()
        return diplome_type

    @staticmethod
    def delete(id: int):
        diplome_type = DiplomeType.objects.get(id=id)
        diplome_type.delete()
        return True