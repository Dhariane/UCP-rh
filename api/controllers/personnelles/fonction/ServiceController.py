import os
from urllib import response 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Services
from api.services import ServiceService
from api.dto.personnelles.fonction.ServiceDto import ServiceDto

class ServiceController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                data=ServiceService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste demandes success",
                    "data": data
                }
                return  Response(response, status=status.HTTP_200_OK)
            except Service.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Service non trouvé pour l'id = {id}",
                    # "error": f"Service non trouvé pour l'id = {id}"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            data= ServiceService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste demandes success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
    def post(self, request):
        valiny = ServiceDto(data=request.data)
        if not valiny.is_valid():
            error_list = []
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    error_list.append(f"{field}: {error}")
            errors_str = "; ".join(error_list)

            response = {
                "status": "error",
                "message": errors_str,
                "errors": valiny.errors
            }


        etat = ServiceService.create(valiny.validated_data["nom"])
        response = {
                "status": "success",
                "message": "Insertion reussis avec succes",
                "data": ServiceDto(etat).data     
            }
        return Response(response, status=status.HTTP_201_CREATED)


class ServiceCRUDController(APIView):

    def get(self, request):
        services = Services.objects.all().order_by('nom')
        data = [{"id": s.id, "nom": s.nom} for s in services]
        return Response({"data": data})

    def post(self, request):
        nom = request.data.get('nom')
        if not nom:
            return Response({"error": "Nom obligatoire"}, status=400)
        s = Services.objects.create(nom=nom)
        return Response({"status": "success", "data": {"id": s.id, "nom": s.nom}}, status=201)

    def patch(self, request, id):
        try:
            s     = Services.objects.get(id=id)
            s.nom = request.data.get('nom', s.nom)
            s.save()
            return Response({"status": "success", "message": "Service mis à jour"})
        except Services.DoesNotExist:
            return Response({"error": "Service introuvable"}, status=404)

    def delete(self, request, id):
        try:
            Services.objects.get(id=id).delete()
            return Response({"status": "success", "message": "Service supprimé"})
        except Services.DoesNotExist:
            return Response({"error": "Service introuvable"}, status=404)