from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.permission.permissionModel import Permissions
# Assure-toi que ce fichier existe RÉELLEMENT à cet endroit précis
from api.dto.permission.permissionDto import PermissionDto 

class PermissionController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                permission = Permissions.objects.get(id=id)
                # On utilise le "DTO" comme un Serializer ici
                serializer = PermissionDto(permission)
                return Response(serializer.data)
            except Permissions.DoesNotExist:
                return Response({"error": "Non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        # CORRECTION ICI : order_by au lieu de order_True
        permissions = Permissions.objects.all().order_by('-id')
        serializer = PermissionDto(permissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PermissionDto(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            return Response({"error": "ID requis"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            permission = Permissions.objects.get(id=id)
            permission.delete()
            return Response({"message": "Supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        except Permissions.DoesNotExist:
            return Response({"error": "Non trouvé"}, status=status.HTTP_404_NOT_FOUND)    