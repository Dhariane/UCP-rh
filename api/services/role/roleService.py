from api.models.role.roleModel import Role
from api.dto.role.roleDto import RoleDTO

class RoleService:
    @staticmethod
    def getAllDto():
        roles = Role.objects.all()
        return RoleDTO(roles, many=True)

    @staticmethod
    def getByIdDto(id):
        role = Role.objects.get(id=id)
        return RoleDTO(role)

    @staticmethod
    def create(name):
        return Role.objects.create(name=name)