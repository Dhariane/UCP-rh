from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models.fonction.contrat import Contrat
from api.services.personnelles.fonction.contratService import ContratService
from api.dto.personnelles.fonction.contratDto import ContratDto

class ContratController(APIView):
    def get(self, request, id=None):
        if id:
            try:
                data = ContratService.getByIdDto(id).data
                response = {
                    "status": "success",
                    "message": "Contrat récupéré avec succès",
                    "data": data
                }
                return Response(response, status=status.HTTP_200_OK)
            except Contrat.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": f"Contrat non trouvé pour l'id = {id}"
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            data = ContratService.getAllDto().data
            response = {
                "status": "success",
                "message": "Liste des contrats récupérée",
                "data": data
            }
            return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        valiny = ContratDto(data=request.data)
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

        contrat = ContratService.create(valiny.validated_data)
        response = {
            "status": "success",
            "message": "Insertion réussie avec succès",
            "data": ContratDto(contrat).data
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request, id):
        valiny = ContratDto(data=request.data, partial=True)
        if not valiny.is_valid():
            return Response(valiny.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            validated = valiny.validated_data
            contrat = ContratService.update(
                id,
                NumeroContrat=validated.get("NumeroContrat"),
                photoContrat=validated.get("photoContrat"),
                typeContrat=validated.get("typeContrat"),
                personnelle=validated.get("personnelle"),
                fonction=validated.get("fonction"),
                dateDebut=validated.get("dateDebut"),
                dateFin=validated.get("dateFin"),
                financement=validated.get("financement"),
                periodeEssai=validated.get("periodeEssai"),
                dateFinEssai=validated.get("dateFinEssai"),
                salaire=validated.get("salaire")
            )
            return Response(ContratDto(contrat).data, status=status.HTTP_200_OK)
        except Contrat.DoesNotExist:
            response = {
                "status": "error",
                "message": f"Contrat non trouvé pour l'id = {id}"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        """
        Déclenché spécifiquement lors du changement de financement / avenant.
        Cette méthode appelle le renouvellement automatique (archivage de l'ancien).
        """
        try:
            # 1. Récupérer le contrat existant pour connaître le 'personnelle_id'
            contrat_actuel = ContratService.getById(id)
            personnelle_id = contrat_actuel.personnelle.id
            
            # 2. On valide les nouvelles données envoyées par Next.js (ex: le nouveau financement)
            valiny = ContratDto(data=request.data, partial=True)
            if not valiny.is_valid():
                return Response({
                    "status": "error",
                    "message": "Données invalides",
                    "errors": valiny.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. On appelle notre méthode de service qui gère la bascule/l'archivage
            nouveau_contrat = ContratService.changer_statut_carriere(
                personnelle_id=personnelle_id,
                nouvelles_data=valiny.validated_data
            )

            response = {
                "status": "success",
                "message": "Ancien contrat archivé et nouveau mode de financement activé.",
                "data": ContratDto(nouveau_contrat).data
            }
            return Response(response, status=status.HTTP_200_OK)

        except Contrat.DoesNotExist:
            return Response({
                "status": "error",
                "message": f"Contrat initial non trouvé pour l'id = {id}"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Erreur lors de l'archivage : {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        