from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Photos
from api.services.personnelles.propos.photosService import PhotosService
from api.dto.personnelles.propos.photosDto import PhotosDto

class PhotosController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                data = PhotosService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Photo trouvée avec succès",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Photos.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Photo non trouvée pour l'id = {id}",
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = PhotosService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste des photos récupérée avec succès",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        valiny = PhotosDto(data=request.data)
        if not valiny.is_valid():
            errors_list = []
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    errors_list.append(f"{field}: {error}")

            errors_str = "; ".join(errors_list)

            response = {
                "status": "error",
                "message": errors_str,
                "errors": valiny.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        photo = PhotosService.create(
            valiny.validated_data["nom"],
            valiny.validated_data["data"],
            valiny.validated_data["personnelle"]
        )
        response = {
            "status": "success",
            "message": "Photo créée avec succès",
            "data": PhotosService.getByIdDto(photo.id).data
        }

        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id): 
        valiny = PhotosDto(data=request.data)
        if not valiny.is_valid():
            errors_list = []
            for field, field_errors in valiny.errors.items():
                for error in field_errors:
                    errors_list.append(f"{field}: {error}")

            errors_str = "; ".join(errors_list)

            response = {
                "status": "error",
                "message": errors_str,
                "errors": valiny.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            photo = PhotosService.update(
                id,
                valiny.validated_data["data"],
                valiny.validated_data["personnelle"],
                valiny.validated_data["nom"]
            )
            response = {
                "status": "success",
                "message": "Photo mise à jour avec succès",
                "data": PhotosService.getByIdDto(photo.id).data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Photos.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Photo non trouvée pour l'id = {id}",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)