# api/controllers/fonction/fonctionListController.py
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.fonction.fonctions import Fonctions

class FonctionListController(APIView):

    def get(self, request):
        service_id = request.query_params.get('service', None)

        fonctions = Fonctions.objects.all().order_by('nom')

        if service_id:
            fonctions = fonctions.filter(service_id=service_id)  # ← ici le problème

        data = [
            {
                "id":      f.id,
                "nom":     f.nom,
                "is_chef": f.is_chef,
                "service": f.service_id,  # ← retourne null
            }
            for f in fonctions
        ]

        return Response({"data": data})