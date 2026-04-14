from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.conge.soldeConge import SoldeConge
from api.services.conge.soldeCongeService import SoldeCongeServices
from api.dto.conge.soldeCongeDto import SoldeCongeDto


class SoldeCongeController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                obj = SoldeCongeServices.getById(id)
                return Response({"status": "success", "data": SoldeCongeDto(obj).data})
            except SoldeConge.DoesNotExist:
                return Response({"status": "error", "message": "Non trouvé"}, status=404)
        else:
            data = SoldeCongeServices.getAll()
            return Response({
                "status": "success",
                "data": SoldeCongeDto(data, many=True).data
            })

    def post(self, request):
        serializer = SoldeCongeDto(data=request.data)
        if serializer.is_valid():
            obj = SoldeCongeServices.create(serializer.validated_data)
            return Response({
                "status": "success",
                "data": SoldeCongeDto(obj).data
            }, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, id):
        try:
            serializer = SoldeCongeDto(data=request.data, partial=True)
            if serializer.is_valid():
                obj = SoldeCongeServices.update(id, serializer.validated_data)
                return Response({"status": "success", "data": SoldeCongeDto(obj).data})
            return Response(serializer.errors, status=400)
        except SoldeConge.DoesNotExist:
            return Response({"message": "Non trouvé"}, status=404)

    def patch(self, request, id):
        return self.put(request, id)