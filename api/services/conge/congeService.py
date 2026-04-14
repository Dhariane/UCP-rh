from api.models.conge.conge import Conge


class CongeServices:

    @staticmethod
    def getAll():
        return Conge.objects.all().order_by("-created_at")

    @staticmethod
    def getById(id: int) -> Conge:
        return Conge.objects.get(id=id)

    @staticmethod
    def create(data) -> Conge:
        return Conge.objects.create(
            Personnel=data.get("Personnel"),
            typeConge=data.get("typeConge"),
            soldeConge=data.get("soldeConge"),
            dateDebut=data.get("dateDebut"),
            dateFin=data.get("dateFin"),
            nombreJours=data.get("nombreJours"),
            description=data.get("description"),
            statut=data.get("statut")
        )

    @staticmethod
    def update(id: int, data) -> Conge:
        conge = Conge.objects.get(id=id)

        for field, value in data.items():
            if value is not None and hasattr(conge, field):
                setattr(conge, field, value)

        conge.save()
        return conge

    @staticmethod
    def delete(id: int):
        conge = Conge.objects.get(id=id)
        conge.delete()