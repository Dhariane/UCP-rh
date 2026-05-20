from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError

from api.models.conge.congePlanifieModel import CongePlanifie
from api.models.conge.typeConges import TypeConge
from api.models.propos.personnelles import Personnelles
from api.dto.conge.congePlanifieDTO import CongePlanifieDTO

# ─────────────────────────────────────────────────────────────────────────────
# 1. GESTION PAR PERSONNEL (LISTER & CRÉER)
# ─────────────────────────────────────────────────────────────────────────────
class CongePlanifieController(APIView):

    # ✅ GET : Récupérer tous les congés planifiés d'un personnel
    def get(self, request, personnel_id):
        try:
            conges = CongePlanifie.objects.select_related('type_conge').filter(
                personnel_id=personnel_id
            ).order_by('-date_debut')
            serializer = CongePlanifieDTO(conges, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Erreur de récupération : {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST : Planifier un nouveau congé pour un personnel
    def post(self, request, personnel_id):
        try:
            if not Personnelles.objects.filter(id=personnel_id).exists():
                return Response({"error": "Personnel non trouvé"}, status=status.HTTP_404_NOT_FOUND)

            data = request.data
            type_conge_id = data.get('type_conge_id')
            date_debut    = data.get('date_debut')
            date_fin      = data.get('date_fin')
            description   = data.get('description', '')

            if not all([type_conge_id, date_debut, date_fin]):
                return Response({"error": "type_conge_id, date_debut et date_fin sont requis"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                type_conge = TypeConge.objects.get(id=type_conge_id)
            except TypeConge.DoesNotExist:
                return Response({"error": "Le type de congé spécifié n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

            conge_planifie = CongePlanifie(
                personnel_id=personnel_id,
                type_conge=type_conge,
                date_debut=date_debut,
                date_fin=date_fin,
                description=description
            )
            conge_planifie.full_clean()
            conge_planifie.save()

            return Response({
                "status": "success",
                "message": "Congé planifié créé avec succès",
                "id": conge_planifie.id
            }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            error_msg = e.message_dict.get('__all__', [str(e)])[0] if hasattr(e, 'message_dict') else str(e)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ─────────────────────────────────────────────────────────────────────────────
# 2. GESTION PAR CRÉNEAU UNIQUE (GET, MODIFIER & SUPPRIMER)
# ─────────────────────────────────────────────────────────────────────────────
class CongePlanifieDetailController(APIView):

    # ✅ GET : Récupérer un congé planifié par son id
    def get(self, request, id):
        try:
            conge_planifie = CongePlanifie.objects.select_related('type_conge').get(id=id)
            serializer = CongePlanifieDTO(conge_planifie)
            return Response({
                "status": "success",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except CongePlanifie.DoesNotExist:
            return Response({"error": "Congé planifié non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # PATCH : Modifier un congé planifié existant
    def patch(self, request, id):
        try:
            conge_planifie = CongePlanifie.objects.get(id=id)
            data = request.data

            type_conge_id = data.get('type_conge_id')
            if type_conge_id:
                try:
                    conge_planifie.type_conge = TypeConge.objects.get(id=type_conge_id)
                except TypeConge.DoesNotExist:
                    return Response({"error": "Le type de congé spécifié n'existe pas"}, status=status.HTTP_404_NOT_FOUND)

            if 'date_debut'   in data: conge_planifie.date_debut   = data.get('date_debut')
            if 'date_fin'     in data: conge_planifie.date_fin     = data.get('date_fin')
            if 'description'  in data: conge_planifie.description  = data.get('description')

            conge_planifie.full_clean()
            conge_planifie.save()

            serializer = CongePlanifieDTO(conge_planifie)
            return Response({
                "status": "success",
                "message": "Planning modifié avec succès",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        except CongePlanifie.DoesNotExist:
            return Response({"error": "Congé planifié non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            error_msg = e.message_dict.get('__all__', [str(e)])[0] if hasattr(e, 'message_dict') else str(e)
            return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE : Supprimer un congé planifié
    def delete(self, request, id):
        try:
            conge_planifie = CongePlanifie.objects.get(id=id)
            conge_planifie.delete()
            return Response({
                "status": "success",
                "message": "Le congé planifié a été supprimé avec succès"
            }, status=status.HTTP_200_OK)
        except CongePlanifie.DoesNotExist:
            return Response({"error": "Congé planifié non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)