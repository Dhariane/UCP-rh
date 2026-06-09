
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Relations
from api.services.personnelles.contact.RelationService import RelationService
from api.dto.personnelles.contact.RelationDto import RelationDto

class RelationController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                data = RelationService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste relations success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Relations.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Relation non trouvé pour l'id = {id}",
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = RelationService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste relations success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        valiny = RelationDto(data=request.data)
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

        relation = RelationService.create(valiny.validated_data)
        response = {
            "status": "success",
            "message": "Relation créée avec succès",
            "data": RelationService.getByIdDto(relation.id).data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = RelationDto(data=request.data)
        if not valiny.is_valid():
            return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            etat = RelationService.update(id, valiny.validated_data["nom"], valiny.validated_data["grade"])
            return Response(RelationDto(etat).data, status=status.HTTP_200_OK)
        except Relations.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Relation non trouvé pour l'id = {id}",
            }
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Relations
from api.services.personnelles.contact.RelationService import RelationService
from api.dto.personnelles.contact.RelationDto import RelationDto

class RelationController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                data = RelationService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Liste relations success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Relations.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Relation non trouvé pour l'id = {id}",
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            data = RelationService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste relations success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        valiny = RelationDto(data=request.data)
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

        relation = RelationService.create(valiny.validated_data["nom"], valiny.validated_data["grade"])
        response = {
            "status": "success",
            "message": "Relation créée avec succès",
            "data": RelationService.getByIdDto(relation.id).data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        valiny = RelationDto(data=request.data)
        if not valiny.is_valid():
            return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            etat = RelationService.update(id, valiny.validated_data["nom"], valiny.validated_data["grade"])
            return Response(RelationDto(etat).data, status=status.HTTP_200_OK)
        except Relations.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Relation non trouvé pour l'id = {id}",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)