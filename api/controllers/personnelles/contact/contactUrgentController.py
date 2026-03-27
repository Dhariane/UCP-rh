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
        # 1. Validation partielle pour ne pas bloquer sur les champs non modifiés
        valiny = ContactUrgentsDto(data=request.data, partial=True)
        
        if not valiny.is_valid():
            return Response({"status": "error", "errors": valiny.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 2. Récupération de l'instance pour les valeurs par défaut
            instance = ContactUrgences.objects.get(id=id)
            
            # 3. Extraction des données (Nouvelle ou Ancienne)
            nom = valiny.validated_data.get('nom',instance.nom)
            telephone = valiny.validated_data.get('telephone', instance.telephone)
            adresse = valiny.validated_data.get('adresse', instance.adresse)
            
            # Gestion des clés étrangères (on récupère l'ID numérique)
            p_val = valiny.validated_data.get('personnelle', instance.personnelle_id)
            personnelle = p_val.id if hasattr(p_val, 'id') else p_val
            
            r_val = valiny.validated_data.get('relation', instance.relation_id)
            relation = r_val.id if hasattr(r_val, 'id') else r_val

            # 4. Appel du service avec tes variables exactes
            contactUrgence = ContactUrgencesService.update(
                id=id,
                nom=nom,
                telephone=telephone,
                adresse=adresse,
                personnelle=personnelle,
                relation=relation
            )
            
            return Response({
                "status": "success",
                "message": "ContactUrgence updated successfully",
                "data": ContactUrgentsDto(contactUrgence).data
            }, status=status.HTTP_200_OK)

        except ContactUrgences.DoesNotExist:
            return Response({"status": "error", "message": "ContactUrgence not found"}, status=status.HTTP_404_NOT_FOUND)