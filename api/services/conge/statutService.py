from api.models.conge.statut import Statut


class StatutServices:

    @staticmethod
    def getAll():
        return Statut.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> Statut:
        return Statut.objects.get(id=id)

    @staticmethod
    def create(data) -> Statut:
        return Statut.objects.create(
            statut=data.get("statut")
        )

    @staticmethod
    def update(id: int, data) -> Statut:
        obj = Statut.objects.get(id=id)

        for field, value in data.items():
            if value is not None and hasattr(obj, field):
                setattr(obj, field, value)

        obj.save()
        return obj

    @staticmethod
    def delete(id: int):
        obj = Statut.objects.get(id=id)
        obj.delete()