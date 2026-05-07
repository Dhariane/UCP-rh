from api.models.conge.passationservice import PassationService


class PassationServices:

    @staticmethod
    def getAll():
        return PassationService.objects.select_related(
            'titulaire', 'statut', 'remplacant'
        ).all()

    @staticmethod
    def getById(id: int):
        return PassationService.objects.select_related(
            'titulaire', 'statut', 'remplacant'
        ).get(pk=id)

    @staticmethod
    def create(data: dict):
        return PassationService.objects.create(**data)

    @staticmethod
    def update(id: int, data: dict):
        passation = PassationService.objects.get(pk=id)
        for attr, value in data.items():
            setattr(passation, attr, value)
        passation.save()
        return passation

    @staticmethod
    def delete(id: int):
        passation = PassationService.objects.get(pk=id)
        passation.delete()