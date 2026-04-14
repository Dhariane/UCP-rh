from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.conge.statut import Statut
from api.services.conge.statutService import StatutServices
from api.dto.conge.statutDto import StatutDto


class StatutController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                obj = StatutServices.getById(id)
                return Response({
                    "status": "success",
                    "data": StatutDto(obj).data
                }, status=200)
            except Statut.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Statut non trouvé"
                }, status=404)
        else:
            data = StatutServices.getAll()
            return Response({
                "status": "success",
                "data": StatutDto(data, many=True).data
            }, status=200)

    def post(self, request):
        serializer = StatutDto(data=request.data)

        if serializer.is_valid():
            obj = StatutServices.create(serializer.validated_data)
            return Response({
                "status": "success",
                "data": StatutDto(obj).data
            }, status=201)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)

    def put(self, request, id):
        try:
            serializer = StatutDto(data=request.data, partial=True)

            if serializer.is_valid():
                obj = StatutServices.update(id, serializer.validated_data)
                return Response({
                    "status": "success",
                    "data": StatutDto(obj).data
                }, status=200)

            return Response(serializer.errors, status=400)

        except Statut.DoesNotExist:
            return Response({
                "message": "Non trouvé"
            }, status=404)

    def delete(self, request, id):
        try:
            StatutServices.delete(id)
            return Response({
                "status": "success",
                "message": "Supprimé avec succès"
            }, status=200)
        except Statut.DoesNotExist:
            return Response({
                "message": "Non trouvé"
            }, status=404)

    def patch(self, request, id):
        return self.put(request, id)