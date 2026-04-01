from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.contact.contactUrgences import ContactUrgences
from api.services.personnelles.contact.ContactUrgentService import ContactUrgencesService
from api.dto.personnelles.contact.ContactUrgentsDto import ContactUrgentsDto

class ContactUrgentController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                data = ContactUrgencesService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "ContactUrgence retrieved successfully",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except ContactUrgences.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"ContactUrgence not found for id = {id}"
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            data = ContactUrgencesService.getAllDto().data
            response = {
                "status": "success",
                "message": "List of ContactUrgences retrieved successfully",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
        
    def post(self, request):
        valiny = ContactUrgentsDto(data=request.data)
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
        
        contactUrgence = ContactUrgencesService.create(
            nom = valiny.validated_data['nom'],
            telephone=valiny.validated_data['telephone'],
            adresse=valiny.validated_data['adresse'],
            personnelle=valiny.validated_data['personnelle'],
            relation=valiny.validated_data['relation']
        )
        response = {
            "status": "success",
            "message": "ContactUrgence created successfully",
            "data": ContactUrgentsDto(contactUrgence).data
        }
        return Response(response, status=status.HTTP_201_CREATED)
    
    def put(self, request, id):
        # On passe partial=True pour autoriser le PATCH
        serializer = ContactUrgentsDto(data=request.data, partial=True)
        if serializer.is_valid():
            # On envoie tout le dictionnaire validé au service
            instance = ContactUrgencesService.update(id, serializer.validated_data)
            return Response({"status": "success", "data": ContactUrgentsDto(instance).data})
        return Response(serializer.errors, status=400)

    def patch(self, request, id):
        return self.put(request, id)