from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.services.personnelles.diplome.typeDiplomeService import DiplomeTypeService
from api.dto.personnelles.diplome.typeDiplomeDto import TypeDiplomeDTO   # À adapter


class DiplomeTypeController(APIView):

    def get(self, request, id=None):
        try:
            if id:
                diplome_type = DiplomeTypeService.getById(id)
                if not diplome_type:
                    return Response({"error": "Type de diplôme introuvable"}, status=status.HTTP_404_NOT_FOUND)
                return Response(TypeDiplomeDTO(diplome_type).data, status=status.HTTP_200_OK)
            
            diplome_types = DiplomeTypeService.getAll()
            return Response(TypeDiplomeDTO(diplome_types, many=True).data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            diplome_type = DiplomeTypeService.create(request.data)
            return Response({
                "status": "success",
                "message": "Type de diplôme créé avec succès",
                "data": TypeDiplomeDTO(diplome_type).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            diplome_type = DiplomeTypeService.update(id, request.data)
            return Response({
                "status": "success",
                "message": "Mise à jour réussie",
                "data": TypeDiplomeDTO(diplome_type).data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            DiplomeTypeService.delete(id)
            return Response({
                "status": "success",
                "message": "Type de diplôme supprimé avec succès"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)