from api.models.conge.typeConges import TypeConge

class TypeCongeServices:
    
    @staticmethod
    def getAll():
        return TypeConge.objects.all().order_by("libelle")

    @staticmethod
    def getById(id: int):
        return TypeConge.objects.get(id=id)

    @staticmethod
    def create(data):
        return TypeConge.objects.create(
            libelle=data.get('libelle'),
            code=data.get('code'),
            duree_max=data.get('duree_max', None)
        )

    @staticmethod
    def update(id: int, data):
        type_conge = TypeConge.objects.get(id=id)
        
        if 'libelle' in data:
            type_conge.libelle = data['libelle']
        if 'code' in data:
            type_conge.code = data['code']
        if 'duree_max' in data:
            type_conge.duree_max = data['duree_max']
        
        type_conge.save()
        return type_conge