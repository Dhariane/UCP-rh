from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.permission.permissionModel import EvenementPermission, Permissions, SoldePermission
from api.dto.permission.permissionDto import EvenementPermissionDto, PermissionDto, SoldePermissionDto
from api.services.permission.permissionService import PermissionService


# ─────────────────────────────────────────────────────────────────────────────
# GET /evenements-permission/
# Liste des 7 événements (lecture seule, alimenté par SQL)
# ─────────────────────────────────────────────────────────────────────────────
class EvenementPermissionController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                evt = EvenementPermission.objects.get(id=id)
                return Response(EvenementPermissionDto(evt).data)
            except EvenementPermission.DoesNotExist:
                return Response({"error": "Non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        evenements = EvenementPermission.objects.all()
        return Response(EvenementPermissionDto(evenements, many=True).data)


# ─────────────────────────────────────────────────────────────────────────────
# CRUD permissions
# GET    /permissions/              → liste toutes
# GET    /permissions/<id>/         → détail
# POST   /permissions/              → créer une demande
# PATCH  /permissions/<id>/         → approuver / refuser
# DELETE /permissions/<id>/         → supprimer
# ─────────────────────────────────────────────────────────────────────────────
class PermissionController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                permission = Permissions.objects.get(id=id)
                return Response(PermissionDto(permission).data)
            except Permissions.DoesNotExist:
                return Response({"error": "Non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        permissions = Permissions.objects.select_related(
            'personnelle', 'evenement'
        ).all().order_by('-id')
        return Response(PermissionDto(permissions, many=True).data)

    def post(self, request):
        serializer = PermissionDto(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        date_debut = serializer.validated_data['date_debut']
        date_fin = serializer.validated_data['date_fin']
        evenement = serializer.validated_data.get('evenement')

        # Durée : auto depuis l'événement, sinon calcul par dates
        if evenement and evenement.duree_defaut is not None:
            duree = evenement.duree_defaut
        else:
            duree = PermissionService.calculer_duree(date_debut, date_fin)

        serializer.save(duree=duree)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, id=None):
        if not id:
            return Response({"error": "ID requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            nouveau_statut = request.data.get('statut')

            if nouveau_statut == 'Approuvé':
                permission = PermissionService.approuver_permission(id)
                return Response(PermissionDto(permission).data)

            if nouveau_statut == 'Refusé':
                permission = PermissionService.refuser_permission(id)
                return Response(PermissionDto(permission).data)

            # Modification simple (motif, durée pour evt 6&7, etc.)
            permission = Permissions.objects.get(id=id)
            serializer = PermissionDto(permission, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

class SoldePermissionReinitTousController(APIView):
    """POST /solde-permission/reinitialiser-tous/ → remet à 10j tous les employés"""
    def post(self, request):
        from django.utils import timezone
        annee = request.data.get('annee', timezone.now().year)
        soldes = SoldePermission.objects.filter(annee=annee)
        count = soldes.count()
        soldes.update(
            solde_disponible=SoldePermission.SOLDE_MAX,
            date_reinitialisation=timezone.now()
        )
        return Response({
            "message": f"{count} solde(s) réinitialisé(s) à {SoldePermission.SOLDE_MAX}j.",
            "annee": annee,
            "count": count,
        })
# ─────────────────────────────────────────────────────────────────────────────
# Solde permission par employé
# GET  /solde-permission/<personnelle_id>/         → solde de l'année courante
# POST /solde-permission/<personnelle_id>/reinitialiser/ → remet à 10j (RH)
# ─────────────────────────────────────────────────────────────────────────────
class SoldePermissionController(APIView):

    def get(self, request, personnelle_id=None):
        if not personnelle_id:
            # Liste tous les soldes (vue RH)
            soldes = SoldePermission.objects.select_related('personnelle').all()
            return Response(SoldePermissionDto(soldes, many=True).data)

        soldes = SoldePermission.objects.filter(
            personnelle_id=personnelle_id
        ).order_by('-annee')
        return Response(SoldePermissionDto(soldes, many=True).data)


class SoldePermissionReinitController(APIView):
    """
    POST /solde-permission/<personnelle_id>/reinitialiser/
    Body optionnel : { "annee": 2025 }
    """
    def post(self, request, personnelle_id=None):
        if not personnelle_id:
            return Response({"error": "personnelle_id requis"}, status=status.HTTP_400_BAD_REQUEST)

        annee = request.data.get('annee', None)

        try:
            solde = PermissionService.reinitialiser_solde(personnelle_id, annee)
            return Response({
                "message": f"Solde réinitialisé à {SoldePermission.SOLDE_MAX}j.",
                "solde": SoldePermissionDto(solde).data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)