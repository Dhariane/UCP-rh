from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.permission.permissionModel import Permissions
from api.dto.permission.permissionDto import PermissionDto 
from api.services.permission.permissionService import PermissionService

class PermissionController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                permission = Permissions.objects.get(id=id)
                serializer = PermissionDto(permission)
                return Response(serializer.data)
            except Permissions.DoesNotExist:
                return Response({"error": "Non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        permissions = Permissions.objects.all().order_by('-id')
        serializer = PermissionDto(permissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PermissionDto(data=request.data)
        if serializer.is_valid():
            date_debut = serializer.validated_data['date_debut']
            date_fin = serializer.validated_data['date_fin']
            
            # Calcul de la durée au moment de la demande
            duree = PermissionService.calculer_duree(date_debut, date_fin)
            
            # Sauvegarde avec la durée calculée
            serializer.save(duree=duree)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        """
        Approbation par l'admin : Déclenche la déduction du solde.
        """
        if not id:
            return Response({"error": "ID requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nouveau_statut = request.data.get('statut')
            
            if nouveau_statut == 'Approuvé':
                # Appel au service pour gérer solde_initial et solde_restant
                permission = PermissionService.approuver_permission(id)
                serializer = PermissionDto(permission)
                return Response(serializer.data)
            
            # Gestion normale pour Refusé ou modification de motif
            permission = Permissions.objects.get(id=id)
            serializer = PermissionDto(permission, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
                
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            return Response({"error": "ID requis"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            permission = Permissions.objects.get(id=id)
            permission.delete()
            return Response({"message": "Supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        except Permissions.DoesNotExist:
            return Response({"error": "Non trouvé"}, status=status.HTTP_404_NOT_FOUND)