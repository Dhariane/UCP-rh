from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.conge.typeConges import TypeConge
from api.services.conge.typeCongeService import TypeCongeServices
from api.dto.conge.typeCongeDto import TypeCongeDto


class TypeCongeController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                type_conge = TypeCongeServices.getById(id)
                serializer = TypeCongeDto(type_conge)
                return Response({"status": "success", "data": serializer.data}, status=200)
            except TypeConge.DoesNotExist:
                return Response({"status": "error", "message": "Non trouvé"}, status=404)
        else:
            data = TypeCongeServices.getAll()
            serializer = TypeCongeDto(data, many=True)
            return Response({"status": "success", "data": serializer.data}, status=200)

    def post(self, request):
        serializer = TypeCongeDto(data=request.data)
        if serializer.is_valid():
            obj = TypeCongeServices.create(serializer.validated_data)
            return Response({
                "status": "success",
                "data": TypeCongeDto(obj).data
            }, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, id):
        try:
            serializer = TypeCongeDto(data=request.data, partial=True)
            if serializer.is_valid():
                obj = TypeCongeServices.update(id, serializer.validated_data)
                return Response({"status": "success", "data": TypeCongeDto(obj).data})
            return Response(serializer.errors, status=400)
        except TypeConge.DoesNotExist:
            return Response({"message": "Non trouvé"}, status=404)

    def patch(self, request, id):
        return self.put(request, id)