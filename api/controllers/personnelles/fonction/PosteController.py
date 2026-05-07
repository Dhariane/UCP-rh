from  rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Postes
from api.services.personnelles.fonction.PosteService import PosteService
from api.dto.personnelles.fonction.PosteDto import PosteDTO
class PosteController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                poste = PosteService.getById(id)
                data = PosteDTO(poste).data
                response = {
                    "status": "success",
                    "message": "Poste récupéré avec succès",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Poste.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": f"Poste non trouvé pour l'id = {id}"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            postes = PosteService.getAll()
            serializer = PosteDTO(postes, many=True)
            response = {
                "status": "success",
                "message": "Liste des postes récupérée",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        valiny = PosteDTO(data=request.data)
        if not valiny.is_valid():
            # Transformer les erreurs en une seule string séparée par "; "
            errors_list = []
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    errors_list.append(f"{field}: {error}")

            errors_str = "; ".join(errors_list)  # Une seule string

            response = {
                "status": "error",
                "message": errors_str,  # toutes les erreurs dans "message"
                "errors": valiny.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


        etat = PosteService.create(valiny.validated_data["nom"],valiny.validated_data["grade"])
        response = {
                "status": "success",
                "message": "Insertion réussie avec succès",
                "data": PosteDTO(etat).data
            }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = PosteDTO(data=request.data)
        if not valiny.is_valid():
            return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            etat = PosteService.update(id, valiny.validated_data["nom"], valiny.validated_data["grade"])
            return Response(PosteDTO(etat).data, status=status.HTTP_200_OK)
        except Poste.DoesNotExist:
            response ={
                "status":"error",
                "message": f"Poste non trouvé pour l'id ={id}",
                
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)