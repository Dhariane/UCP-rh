from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.role.roleService import RoleService
from api.dto.role.roleDto import RoleDTO

class RoleController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                data = RoleService.getByIdDto(id).data
                return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
            
            except Exception:
                return Response({"status": "error", "message": "Role non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        data = RoleService.getAllDto().data
        return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoleDTO(data=request.data)
        if serializer.is_valid():
            role = RoleService.create(name=serializer.validated_data['name'])
            return Response({"status": "success", "message": "Rôle créé", "data": RoleDTO(role).data}, status=status.HTTP_201_CREATED)
        
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)