from api.models.conge.soldeConge import SoldeConge


class SoldeCongeServices:

    @staticmethod
    def getAll():
        return SoldeConge.objects.all().order_by("id")

    @staticmethod
    def getById(id: int) -> SoldeConge:
        return SoldeConge.objects.get(id=id)

    @staticmethod
    def create(data) -> SoldeConge:
        return SoldeConge.objects.create(
            personnel=data.get("personnel"),
            annee=data.get("annee"),
            total=data.get("total"),
            reste=data.get("reste")
        )

    @staticmethod
    def update(id: int, data) -> SoldeConge:
        solde = SoldeConge.objects.get(id=id)

        for field, value in data.items():
            if value is not None and hasattr(solde, field):
                setattr(solde, field, value)

        solde.save()
        return solde