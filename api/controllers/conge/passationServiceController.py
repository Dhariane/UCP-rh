from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


from api.models.conge.conge import Conge
from api.models.conge.passationservice import PassationService
from api.services.conge.congeService import CongeServices
from api.services.conge.passationServiceService import PassationServices
from api.dto.conge.passationServiceDto import PassationServiceDTO


class PassationServiceController(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, id=None):
        if id:
            try:
                passation = PassationServices.getById(id)
                serializer = PassationServiceDTO(passation)
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except PassationService.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": f"Passation de service non trouvée (ID: {id})"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            passations = PassationServices.getAll()
            serializer = PassationServiceDTO(passations, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PassationServiceDTO(data=request.data)

        if serializer.is_valid():
            try:
                passation = PassationServices.create(serializer.validated_data)
                return Response({
                    "status": "success",
                    "message": "Passation de service créée avec succès",
                    "data": PassationServiceDTO(passation).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            serializer = PassationServiceDTO(data=request.data, partial=True)

            if serializer.is_valid():
                passation = PassationServices.update(id, serializer.validated_data)
                return Response({
                    "status": "success",
                    "message": "Passation de service mise à jour avec succès",
                    "data": PassationServiceDTO(passation).data
                }, status=status.HTTP_200_OK)

            return Response({
                "status": "error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except PassationService.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Passation de service non trouvée (ID: {id})"
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        """
        Appelé par Next.js quand le remplaçant accepte ou refuse la passation (ID de la passation)
        """
        try:
            passation = PassationServices.getById(id)
            decision = request.data.get('decision') # 'approuve' ou 'refuse'
            motif = request.data.get('motif', '')

            # Trouver le congé lié à cette passation de service
            conge = Conge.objects.filter(passation_service=passation).first()
            if not conge:
                return Response({
                    "status": "error",
                    "message": "Aucun congé associé à cette passation."
                }, status=status.HTTP_404_NOT_FOUND)

            if decision == 'approuve':
                # 🚀 On utilise notre service pour basculer chez le chef et notifier !
                CongeServices.accepterPassation(conge.id)
                
                return Response({
                    "status": "success",
                    "message": "Passation acceptée. Le circuit est transmis au chef direct."
                }, status=status.HTTP_200_OK)

            elif decision == 'refuse':
                # Si le remplaçant refuse, le congé est annulé/rejeté directement
                conge.statut_id = 3 # Code ID 3 = Refusé
                conge.etape_validation = 'termine'
                conge.save()
                
                # Mettre à jour le statut de la passation si tu as un champ pour ça
                PassationServices.update(id, {"statut": "refuse"}) 
                
                return Response({
                    "status": "success",
                    "message": "Passation refusée. La demande de congé a été clôturée."
                }, status=status.HTTP_200_OK)

            return Response({
                "status": "error",
                "message": "La décision doit être 'approuve' ou 'refuse'."
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, id):
        try:
            PassationServices.delete(id)
            return Response({
                "status": "success",
                "message": "Passation de service supprimée avec succès"
            }, status=status.HTTP_204_NO_CONTENT)
        except PassationService.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Passation de service non trouvée (ID: {id})"
            }, status=status.HTTP_404_NOT_FOUND)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from api.models.conge.passationservice import PassationService
from api.services.conge.passationServiceService import PassationServices
from api.dto.conge.passationServiceDto import PassationServiceDTO


class PassationServiceController(APIView):
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, id=None):
        if id:
            try:
                passation = PassationServices.getById(id)
                serializer = PassationServiceDTO(passation)
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except PassationService.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": f"Passation de service non trouvée (ID: {id})"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            passations = PassationServices.getAll()
            serializer = PassationServiceDTO(passations, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PassationServiceDTO(data=request.data)

        if serializer.is_valid():
            try:
                passation = PassationServices.create(serializer.validated_data)
                return Response({
                    "status": "success",
                    "message": "Passation de service créée avec succès",
                    "data": PassationServiceDTO(passation).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        try:
            serializer = PassationServiceDTO(data=request.data, partial=True)

            if serializer.is_valid():
                passation = PassationServices.update(id, serializer.validated_data)
                return Response({
                    "status": "success",
                    "message": "Passation de service mise à jour avec succès",
                    "data": PassationServiceDTO(passation).data
                }, status=status.HTTP_200_OK)

            return Response({
                "status": "error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except PassationService.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Passation de service non trouvée (ID: {id})"
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        return self.put(request, id)

    def delete(self, request, id):
        try:
            PassationServices.delete(id)
            return Response({
                "status": "success",
                "message": "Passation de service supprimée avec succès"
            }, status=status.HTTP_204_NO_CONTENT)
        except PassationService.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Passation de service non trouvée (ID: {id})"
            }, status=status.HTTP_404_NOT_FOUND)
