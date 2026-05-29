from rest_framework.views import APIView
from rest_framework.views import    APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.fonction.fonctions import Fonctions
from api.models.fonction.service import Services
from api.services.personnelles.fonction.fonctionService import FonctionService
from api.dto.personnelles.fonction.fonctionDto import FonctionDto

class FonctionController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                data = FonctionService.getByIdDto(id).data
                return Response({
                    "status": "success",
                    "message": "Fonction retrieved successfully",
                    "data": data
                }, status=status.HTTP_200_OK)
            except Fonctions.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": f"Fonction not found for id = {id}"
                }, status=status.HTTP_404_NOT_FOUND)
                response = {
                    "status": "error",
                    "message": f"Fonction not found for id = {id}"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            data = FonctionService.getAllDto().data
            return Response({
                "status": "success",
                "message": "List of Fonctions retrieved successfully",
                "data": data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        valiny = FonctionDto(data=request.data)
        if not valiny.is_valid():
            return Response({"status": "error", "errors": valiny.errors}, status=status.HTTP_400_BAD_REQUEST)

        fonction = FonctionService.create(valiny.validated_data)
        return Response({
            "status": "success",
            "message": "Fonction created successfully",
            "data": FonctionDto(fonction).data
        }, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        valiny = FonctionDto(data=request.data, partial=True)
        if not valiny.is_valid():
            return Response({"status": "error", "errors": valiny.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            fonction = FonctionService.update(id, **valiny.validated_data)
            return Response({
                "status": "success",
                "message": "Fonction updated successfully",
                "data": FonctionDto(fonction).data
            }, status=status.HTTP_200_OK)
        except Fonctions.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Fonction not found for id = {id}"
            }, status=status.HTTP_404_NOT_FOUND)


class FonctionCRUDController(APIView):

    def get(self, request):
        service_id = request.query_params.get('service', None)
        fonctions  = Fonctions.objects.select_related(
            'service', 'chef_direct'
        ).all().order_by('service__nom', 'nom')

        if service_id:
            fonctions = fonctions.filter(service_id=service_id)

        data = [
            {
                "id":              f.id,
                "nom":             f.nom,
                "is_chef":         f.is_chef,
                "service":         f.service_id,
                "service_nom":     f.service.nom if f.service else "—",
                "chef_direct":     f.chef_direct_id,
                "chef_direct_nom": f.chef_direct.nom if f.chef_direct else "—",
            }
            for f in fonctions
        ]
        return Response({"data": data})

    def patch(self, request, id):
        try:
            f = Fonctions.objects.get(id=id)

            # ── Champs simples ───────────────────────────────────
            f.nom     = request.data.get('nom',     f.nom)
            f.is_chef = request.data.get('is_chef', f.is_chef)

            # ── Service ──────────────────────────────────────────
            service_id = request.data.get('service')
            if service_id:
                try:
                    f.service = Services.objects.get(id=service_id)
                except Services.DoesNotExist:
                    pass
            elif service_id == '' or service_id is None and 'service' in request.data:
                f.service = None

            # ── Chef direct ──────────────────────────────────────
            # ✅ On ne touche à chef_direct QUE si le champ est
            #    explicitement présent dans la requête
            if 'chef_direct' in request.data:
                chef_id = request.data.get('chef_direct')
                if chef_id:
                    try:
                        f.chef_direct = Fonctions.objects.get(id=chef_id)
                    except Fonctions.DoesNotExist:
                        return Response(
                            {"error": f"Chef direct introuvable pour id={chef_id}"},
                            status=400
                        )
                else:
                    # chef_id vide ou null → sommet hiérarchique, pas de chef
                    f.chef_direct = None

            f.save()

            return Response({
                "status":  "success",
                "message": "Fonction mise à jour",
                "data": {
                    "id":              f.id,
                    "nom":             f.nom,
                    "is_chef":         f.is_chef,
                    "service":         f.service_id,
                    "service_nom":     f.service.nom if f.service else "—",
                    "chef_direct":     f.chef_direct_id,
                    "chef_direct_nom": f.chef_direct.nom if f.chef_direct else "—",
                }
            })

        except Fonctions.DoesNotExist:
            return Response({"error": "Fonction introuvable"}, status=404)

    def post(self, request):
        nom        = request.data.get('nom')
        is_chef    = request.data.get('is_chef', False)
        service_id = request.data.get('service')
        chef_id    = request.data.get('chef_direct')

        if not nom:
            return Response({"error": "Nom obligatoire"}, status=400)

        service = None
        if service_id:
            try:
                service = Services.objects.get(id=service_id)
            except Services.DoesNotExist:
                return Response({"error": "Service introuvable"}, status=400)

        chef_direct = None
        if chef_id:
            try:
                chef_direct = Fonctions.objects.get(id=chef_id)
            except Fonctions.DoesNotExist:
                return Response({"error": "Chef direct introuvable"}, status=400)

        f = Fonctions.objects.create(
            nom         = nom,
            is_chef     = is_chef,
            service     = service,
            chef_direct = chef_direct,   # ✅ inclus à la création aussi
        )
        return Response({
            "status": "success",
            "data": {
                "id":              f.id,
                "nom":             f.nom,
                "is_chef":         f.is_chef,
                "service":         f.service_id,
                "chef_direct":     f.chef_direct_id,
                "chef_direct_nom": f.chef_direct.nom if f.chef_direct else "—",
            }
        }, status=201)

    def delete(self, request, id):
        try:
            Fonctions.objects.get(id=id).delete()
            return Response({"status": "success", "message": "Fonction supprimée"})
        except Fonctions.DoesNotExist:
            return Response({"error": "Fonction introuvable"}, status=404)
