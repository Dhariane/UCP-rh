from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Cins
from api.services.personnelles.propos.CinsService import CinsService
from api.dto.personnelles.propos.CinsDto import CinsDTO

class CinsController(APIView):

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
        # 1. On autorise la mise à jour partielle (évite l'erreur "champ obligatoire")
        valiny = CinsDTO(data=request.data, partial=True)
        
        if not valiny.is_valid():
            return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 2. On récupère l'objet existant pour avoir les anciennes valeurs
            instance = Cins.objects.get(id=id)
            
            # 3. On extrait les données : la nouvelle si présente, sinon l'ancienne
            # .get() sur validated_data ne renvoie que ce qui a été envoyé dans la requête
            numero = valiny.validated_data.get('numeroCin', instance.numeroCin)
            date = valiny.validated_data.get('dateCin', instance.dateCin)
            lieu = valiny.validated_data.get('lieuCin', instance.lieuCin)
            numDup = valiny.validated_data.get('numeroDuplicata', instance.numeroDuplicata)
            dateDup = valiny.validated_data.get('dateDuplicata',instance.dateDuplicata)
            lieuDup = valiny.validated_data.get('lieuDuplicata',instance.lieuDuplicata)
            # 4. On appelle ton service avec des données complètes (anciennes + nouvelles)
            etat = CinsService.update(
                id,
                numero,
                date,
                lieu,
                numDup,   # Ajouté ici
                dateDup, 
                lieuDup
            )
            
            # 5. On retourne la réponse (en supposant que CinsService(etat).data est ton sérialiseur de sortie)
            return Response(CinsDTO(etat).data, status=status.HTTP_200_OK)
        
        except Cins.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Cins non trouvé pour l'id = {id}",
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            # Sécurité supplémentaire pour voir d'autres erreurs éventuelles
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)