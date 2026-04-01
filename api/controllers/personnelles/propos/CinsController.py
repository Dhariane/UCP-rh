from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.renderers import JSONRenderer

from api.models import Cins
from api.services.personnelles.propos.CinsService import CinsService
from api.dto.personnelles.propos.CinsDto import CinsDTO

class CinsController(APIView):

    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, id=None):
        if id:
            try:
                poste = CinsService.getById(id)
                data = CinsDTO(poste).data
                response = {
                    "status": "success",
                    "message": "Liste cins success",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Cins.DoesNotExist:
                response = {
                    "status": "error",
                    "message": f"Cins non trouvé pour l'id = {id}",
                }

                return Response(response,
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            cins = CinsService.getAll()
            data = CinsDTO(cins, many=True).data
            response = {
                "status": "success",
                "message": "Liste cins success",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)
    def post(self, request):
        serializer = CinsDTO(data=request.data)

        if serializer.is_valid():
            cins = serializer.save()

            return Response({
                "status": "success",
                "message": "Cins créées avec succès",
                "data": CinsDTO(cins).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            # 1. On récupère l'objet actuel
            instance = Cins.objects.get(id=id)
            data = request.data.copy()

            # 2. NETTOYAGE CRITIQUE
            # Si le numeroCin envoyé est le même que celui stocké, on le SUPPRIME 
            # des données de mise à jour pour que SQL ne tente pas de le modifier.
            if 'numeroCin' in data:
                if str(data['numeroCin']) == str(instance.numeroCin):
                    data.pop('numeroCin') # On l'enlève, il est déjà identique en base
            
            # On remplace les chaînes vides par None pour les dates
            for key in list(data.keys()):
                if data[key] == "":
                    data[key] = None

            # 3. VALIDATION
            serializer = CinsDTO(instance, data=data, partial=True)
            
            if serializer.is_valid():
                # On utilise les données validées qui ne contiennent plus le 'numeroCin' gênant
                cin = CinsService.update(id, serializer.validated_data)
                return Response({
                    "status": "success",
                    "data": CinsDTO(cin).data
                })
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Cins.DoesNotExist:
            return Response({"error": "CIN non trouvé"}, status=404)
        except Exception as e:
            # On attrape l'IntegrityError ici pour éviter le crash 500
            return Response({"error": str(e)}, status=400)
    def patch(self, request, id):
        print("DONNÉES REÇUES :", request.data) # Regarde ta console Django
        return self.put(request, id)