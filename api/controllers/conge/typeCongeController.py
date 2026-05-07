from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from api.models.conge.typeConges import TypeConge
from api.services.conge.typeCongeService import TypeCongeServices
from api.dto.conge.typeCongeDto import TypeCongeDTO

class TypeCongeController(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, id=None):
        if id:
            try:
                obj = TypeCongeServices.getById(id)
                serializer = TypeCongeDTO(obj)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except TypeConge.DoesNotExist:
                return Response({"status": "error", "message": "Type non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        else:
            objs = TypeCongeServices.getAll()
            serializer = TypeCongeDTO(objs, many=True)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TypeCongeDTO(data=request.data)
        if serializer.is_valid():
            obj = TypeCongeServices.create(serializer.validated_data)
            return Response({
                "status": "success",
                "message": "Type de congé créé avec succès",
                "data": TypeCongeDTO(obj).data
            }, status=status.HTTP_201_CREATED)
        return Response({"status": "error", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            serializer = TypeCongeDTO(data=request.data, partial=True)
            if serializer.is_valid():
                obj = TypeCongeServices.update(id, serializer.validated_data)
                return Response({
                    "status": "success",
                    "data": TypeCongeDTO(obj).data
                }, status=status.HTTP_200_OK)
            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except TypeConge.DoesNotExist:
            return Response({"message": "Non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        return self.put(request, id)