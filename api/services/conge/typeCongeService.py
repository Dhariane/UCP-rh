from api.models.conge.typeConges import TypeConge


class TypeCongeServices:

    @staticmethod
    def getAll():
        return TypeConge.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> TypeConge:
        return TypeConge.objects.get(id=id)

    @staticmethod
    def create(data) -> TypeConge:
        return TypeConge.objects.create(
            libelle=data.get("libelle")
        )

    @staticmethod
    def update(id: int, data) -> TypeConge:
        type_conge = TypeConge.objects.get(id=id)

        for field, value in data.items():
            if value is not None and hasattr(type_conge, field):
                setattr(type_conge, field, value)

        type_conge.save()
        return type_conge