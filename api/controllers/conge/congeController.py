from xml.dom import ValidationErr

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from api.models.auth.login.loginModel import Login
from api.models.conge.conge import Conge
from api.models.fonction.contrat import Contrat
from api.services.conge.congeService import CongeServices   # Ajuste le chemin selon ton architecture
from api.dto.conge.congeDto import CongeDTO                # Ajuste le chemin


class CongeController(APIView):
    # Parser pour supporter JSON + éventuels fichiers (si tu ajoutes des justificatifs plus tard)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request, id=None):
        if id:
            try:
                conge = CongeServices.getById(id)
                serializer = CongeDTO(conge)
                return Response({
                    "status": "success",
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            except Conge.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": f"Demande de congé non trouvée (ID: {id})"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            # Liste toutes les demandes
            conges = CongeServices.getAll()
            serializer = CongeDTO(conges, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

    from django.core.exceptions import ValidationError 

    def post(self, request):
        """Créer une nouvelle demande de congé"""
        serializer = CongeDTO(data=request.data)

        if serializer.is_valid():
            try:
                conge = CongeServices.create(serializer.validated_data)
                
                return Response({
                    "status": "success",
                    "message": "Demande de congé créée avec succès",
                    "data": CongeDTO(conge).data
                }, status=status.HTTP_201_CREATED)
                
            except ValidationErr as ve:
                # ✅ Capte les levées de clean() (ex: "Vous devez garder au moins 10 jours...")
                return Response({
                    "status": "error",
                    "message": ve.message if hasattr(ve, 'message') else str(ve.messages[0] if hasattr(ve, 'messages') else ve)
                }, status=status.HTTP_400_BAD_REQUEST)
                
            except Exception as e:
                # Capture le reste des vrais plantages système
                return Response({
                    "status": "error",
                    "message": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id):
        """Mettre à jour une demande de congé"""
        try:
            serializer = CongeDTO(data=request.data, partial=True)
            
            if serializer.is_valid():
                conge = CongeServices.update(id, serializer.validated_data)
                return Response({
                    "status": "success",
                    "message": "Demande mise à jour avec succès",
                    "data": CongeDTO(conge).data
                }, status=status.HTTP_200_OK)
            
            return Response({
                "status": "error",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        except Conge.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Demande de congé non trouvée"
            }, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        """Support explicite de la méthode PATCH"""
        return self.put(request, id)
    
    def delete(self, request, id):
        try:
            CongeServices.delete(id)
            return Response({
                    "status": "success",
                    "message": "Demande supprimée avec succès",
            },status=status.HTTP_204_NO_CONTENT)
        except Conge.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Demande de congé non trouvée (ID: {id})"
            }, status=status.HTTP_404_NOT_FOUND)

class CongesEnAttenteController(APIView):
    def get(self, request, login_id):
        try:
            # 1. Trouver le personnel lié au compte connecté
            user_login = Login.objects.get(id=login_id)
            personnel_connecte = user_login.personnelle  # L'instance d'employé

            # 2. Filtrer les congés selon l'étape et le rôle de l'utilisateur connecté
            
            # Cas A : Étape passation -> L'utilisateur connecté est le remplaçant
            conges_passation = Conge.objects.filter(
                etape_validation='passation',
                passation_service__remplacant=personnel_connecte
            )

            # Cas B : Étape chef -> L'utilisateur connecté est le chef direct du demandeur
            # On cherche les contrats actifs où le chef_direct correspond à la fonction actuelle de l'utilisateur
            contrat_actif_user = Contrat.objects.filter(personnelle=personnel_connecte, is_actif=True).first()
            conges_chef = Conge.objects.none()
            
            if contrat_actif_user and contrat_actif_user.fonction:
                fonction_user = contrat_actif_user.fonction
                # On récupère les congés des employés dont le chef direct est l'utilisateur connecté
                conges_chef = Conge.objects.filter(
                    etape_validation='chef',
                    personnel__contrats__fonction__chef_direct=fonction_user,
                    personnel__contrats__is_actif=True
                ).distinct()

            # 3. Fusionner les requêtes
            conges_en_attente = conges_passation | conges_chef
            
            # Trier par date de création décroissante
            conges_en_attente = conges_en_attente.order_by('-created_at')

            serializer = CongeDTO(conges_en_attente, many=True)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except Login.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Utilisateur non trouvé"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)