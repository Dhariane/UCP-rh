from api.models import Experience
from api.dto.personnelles.diplome.experinceDto import ExperienceDTO

class ExperienceService:
    
    @staticmethod
    def create(data) -> Experience:
        return Experience.objects.create(
            entreprise=data['entreprise'],
            poste=data['poste'],
            datedebut=data['datedebut'],
            datefin=data['datefin'],
            description=data['description'],
            personnelle_id=data['personnelle'] # On utilise l'ID de la relation
        )

    @staticmethod
    def getAll():
        return Experience.objects.all().order_by("-datedebut")

    @staticmethod
    def getById(id: int) -> Experience:
        return Experience.objects.get(id=id)

    @staticmethod
    def update(id: int, data: dict) -> Experience:
        experience = Experience.objects.get(id=id)
        for key, value in data.items():
            if hasattr(experience, key):
                setattr(experience, key, value)
        experience.save()
        return experience

    @staticmethod
    def delete(id: int):
        experience = Experience.objects.get(id=id)
        experience.delete()
        return True