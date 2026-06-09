from xml.dom import ValidationErr

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from api.models.auth.login.loginModel import Login
from api.models.conge.conge import Conge
from api.models.fonction.contrat import Contrat
from api.models.propos.personnelles import Personnelles
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

    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status
    from django.shortcuts import get_object_or_404
class CongesEnAttenteController(APIView):
        def get(self, request, login_id=None):
            try:
                if not login_id:
                    return Response({"status": "error", "message": "ID manquant"}, status=400)

                login = None

                # ✅ Si c'est un email
                if isinstance(login_id, str) and '@' in str(login_id):
                    from api.models.propos.propos import Propos
                    propos = Propos.objects.filter(email=login_id).first()
                    if propos:
                        login = Login.objects.filter(email=propos).first()
                else:
                    # Chercher par login_id puis par personnel_id
                    login = Login.objects.filter(id=login_id).first()
                    if not login:
                        personnel = Personnelles.objects.filter(id=login_id).first()
                        if personnel:
                            login = Login.objects.filter(personnelle=personnel).first()

                if not login:
                    return Response({"status": "success", "data": [], 
                                "debug": f"Aucun login pour {login_id}"}, status=200)

                # ... reste du code inchangé

                role_name = login.role.name if login.role else ''
                personnel_connecte = login.personnelle  # ✅ direct via le lien

                # Initialiser toutes les variables
                conges_passation = Conge.objects.none()
                conges_chef      = Conge.objects.none()
                conges_gp_rf     = Conge.objects.none()
                conges_cn        = Conge.objects.none()
                conges_rh        = Conge.objects.none()

                if personnel_connecte:
                    conges_passation = Conge.objects.filter(
                        etape_validation='passation',
                        passation_service__remplacant=personnel_connecte
                    )

                if role_name == 'Chef' and personnel_connecte:
                    contrat_chef = Contrat.objects.filter(
                        personnelle=personnel_connecte, is_actif=True
                    ).first()
                    if contrat_chef:
                        subordonnes = Personnelles.objects.filter(
                            contrats__fonction__chef_direct=contrat_chef.fonction,
                            contrats__is_actif=True
                        )
                        conges_chef = Conge.objects.filter(
                            etape_validation='chef',
                            personnel__in=subordonnes
                        )

                if role_name in ('GP', 'RF'):
                    conges_gp_rf = Conge.objects.filter(etape_validation='gp_rf')

                if role_name == 'CN':
                    conges_cn = Conge.objects.filter(etape_validation='cn')

                if role_name in ('RH', 'admin', 'Superadmin'):
                    conges_rh = Conge.objects.filter(etape_validation='rh')

                ids = (
                    list(conges_passation.values_list('id', flat=True)) +
                    list(conges_chef.values_list('id', flat=True)) +
                    list(conges_gp_rf.values_list('id', flat=True)) +
                    list(conges_cn.values_list('id', flat=True)) +
                    list(conges_rh.values_list('id', flat=True))
                )

                conges = Conge.objects.filter(id__in=ids).order_by('-created_at')
                serializer = CongeDTO(conges, many=True)
                return Response({"status": "success", "data": serializer.data}, status=200)

            except Exception as e:
                return Response({"status": "error", "message": str(e)}, status=500)
