
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.dto.conge import soldeCongeDto
from api.models.conge.soldeConge import SoldeConge
from api.services.conge.soldeCongeService import SoldeCongeServices
from api.dto.conge.soldeCongeDto import SoldeCongeDTO


class SoldeCongeController(APIView):

    # api/controllers/conge/soldeController.py
    def get(self, request):
        from api.models.propos.personnelles import Personnelles
        annee = int(request.query_params.get('annee', timezone.now().year))

        personnels = Personnelles.objects.all()
        data = []

        for p in personnels:
            solde = SoldeConge.objects.filter(
                personnel=p,
                annee=annee
            ).first()

            if solde:
                data.append({
                    "id":           solde.id,
                    "personnel_id": p.id,
                    "nom":          p.nom,
                    "prenom":       p.prenom,
                    "annee":        solde.annee,
                    "total":        solde.total,
                    "utilise":      solde.utilise,
                    "reste":        solde.reste,
                    "is_manual":    solde.is_manual,
                })
            else:
                # ✅ Personnel sans solde → afficher avec 0
                data.append({
                    "id":           None,
                    "personnel_id": p.id,
                    "nom":          p.nom,
                    "prenom":       p.prenom,
                    "annee":        annee,
                    "total":        0,
                    "utilise":      0,
                    "reste":        0,
                    "is_manual":    False,
                })

        return Response({"status": "success", "data": data})

    def put(self, request, id):
        try:
            instance = SoldeCongeServices.getById(id)  # ← récupérer l'instance
            serializer = SoldeCongeDTO(instance, data=request.data, partial=True)  # ← passer l'instance
            if serializer.is_valid():
                obj = SoldeCongeServices.update(id, serializer.validated_data)
                return Response({"status": "success", "data": SoldeCongeDTO(obj).data})
            return Response(serializer.errors, status=400)
        except SoldeConge.DoesNotExist:
            return Response({"message": "Non trouvé"}, status=404)

    def patch(self, request, id):
        return self.put(request, id)
    

# api/controllers/conge/soldeController.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.conge.soldeConge import SoldeConge
from api.models.propos.personnelles import Personnelles
from django.utils import timezone

class SoldeCongeRHController(APIView):

    # api/controllers/conge/soldeController.py
    def get(self, request):
        from api.models.propos.personnelles import Personnelles
        annee = int(request.query_params.get('annee', timezone.now().year))

        personnels = Personnelles.objects.all()
        data = []

        for p in personnels:
            solde = SoldeConge.objects.filter(
                personnel=p,
                annee=annee
            ).first()

            if solde:
                data.append({
                    "id":           solde.id,
                    "personnel_id": p.id,
                    "nom":          p.nom,
                    "prenom":       p.prenom,
                    "annee":        solde.annee,
                    "total":        solde.total,
                    "utilise":      solde.utilise,
                    "reste":        solde.reste,
                    "is_manual":    solde.is_manual,
                })
            else:
                # ✅ Personnel sans solde → afficher avec 0
                data.append({
                    "id":           None,
                    "personnel_id": p.id,
                    "nom":          p.nom,
                    "prenom":       p.prenom,
                    "annee":        annee,
                    "total":        0,
                    "utilise":      0,
                    "reste":        0,
                    "is_manual":    False,
                })

        return Response({"status": "success", "data": data})
    def patch(self, request, solde_id):
        """Modifier ou ajouter des jours au solde"""
        try:
            solde  = SoldeConge.objects.get(id=solde_id)
            action = request.data.get('action')  # 'modifier' ou 'ajouter'
            jours  = int(request.data.get('jours', 0))

            if jours <= 0:
                return Response({
                    "status":  "error",
                    "message": "Le nombre de jours doit être positif"
                }, status=status.HTTP_400_BAD_REQUEST)

            if action == 'modifier':
                # ✅ Remplacer le total
                solde.total     = min(jours, 72)
                solde.is_manual = True

            elif action == 'ajouter':
                # ✅ Ajouter au total existant
                solde.total     = min(solde.total + jours, 72)
                solde.is_manual = True

            else:
                return Response({
                    "status":  "error",
                    "message": "Action invalide — utilisez 'modifier' ou 'ajouter'"
                }, status=status.HTTP_400_BAD_REQUEST)

            solde.save()

            return Response({
                "status":  "success",
                "message": f"Solde mis à jour → {solde.total}j",
                "data": {
                    "id":        solde.id,
                    "total":     solde.total,
                    "utilise":   solde.utilise,
                    "reste":     solde.reste,
                    "is_manual": solde.is_manual,
                }
            })

        except SoldeConge.DoesNotExist:
            return Response({
                "status":  "error",
                "message": "Solde introuvable"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status":  "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.dto.conge import soldeCongeDto
from api.models.conge.soldeConge import SoldeConge
from api.services.conge.soldeCongeService import SoldeCongeServices
from api.dto.conge.soldeCongeDto import SoldeCongeDTO


class SoldeCongeController(APIView):

    def get(self, request, id=None):
        if id:
            try:
                obj = SoldeCongeServices.getById(id)
                return Response({"status": "success", "data": SoldeCongeDTO(obj).data})
            except SoldeConge.DoesNotExist:
                return Response({"status": "error", "message": "Non trouvé"}, status=404)
        else:
            data = SoldeCongeServices.getAll()
            return Response({
                "status": "success",
                "data": SoldeCongeDTO(data, many=True).data
            })

    def post(self, request):
        serializer = SoldeCongeDTO(data=request.data)
        if serializer.is_valid():
            obj = SoldeCongeServices.create(serializer.validated_data)
            return Response({
                "status": "success",
                "data": SoldeCongeDTO(obj).data
            }, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, id):
        try:
            instance = SoldeCongeServices.getById(id)  # ← récupérer l'instance
            serializer = SoldeCongeDTO(instance, data=request.data, partial=True)  # ← passer l'instance
            if serializer.is_valid():
                obj = SoldeCongeServices.update(id, serializer.validated_data)
                return Response({"status": "success", "data": SoldeCongeDTO(obj).data})
            return Response(serializer.errors, status=400)
        except SoldeConge.DoesNotExist:
            return Response({"message": "Non trouvé"}, status=404)

    def patch(self, request, id):
        return self.put(request, id)
