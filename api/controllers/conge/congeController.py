from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.conge.conge import Conge
from api.services.conge.congeService import CongeServices
from api.dto.conge.congeDto import CongeDto


class CongeController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                obj = CongeServices.getById(id)
                return Response({"status": "success", "data": CongeDto(obj).data})
            except Conge.DoesNotExist:
                return Response({"status": "error", "message": "Non trouvé"}, status=404)
        else:
            data = CongeServices.getAll()
            return Response({
                "status": "success",
                "data": CongeDto(data, many=True).data
            })

    def post(self, request):
        serializer = CongeDto(data=request.data)
        if serializer.is_valid():
            try:
                obj = CongeServices.create(serializer.validated_data)
                return Response({
                    "status": "success",
                    "data": CongeDto(obj).data
                }, status=201)
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=500)

        return Response(serializer.errors, status=400)

    def put(self, request, id):
        try:
            serializer = CongeDto(data=request.data, partial=True)
            if serializer.is_valid():
                obj = CongeServices.update(id, serializer.validated_data)
                return Response({"status": "success", "data": CongeDto(obj).data})
            return Response(serializer.errors, status=400)
        except Conge.DoesNotExist:
            return Response({"message": "Non trouvé"}, status=404)

    def delete(self, request, id):
        try:
            CongeServices.delete(id)
            return Response({"status": "success", "message": "Supprimé"})
        except Conge.DoesNotExist:
            return Response({"message": "Non trouvé"}, status=404)

    def patch(self, request, id):
        return self.put(request, id)