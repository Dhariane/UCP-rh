# api/controllers/fonction/superieurController.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models.fonction.fonctions import Fonctions
from api.models.auth.login.loginModel import Login
from api.models.propos.personnelles import Personnelles

class SuperieurController(APIView):

    def get(self, request):
        """Liste tous les personnels avec leurs supérieurs"""
        fonctions = Fonctions.objects.select_related(
            'personnelle', 'service'
        ).prefetch_related(
            'superieurs__personnelle'
        ).filter(dateFin__isnull=True)

        data = []
        for f in fonctions:
            data.append({
                "fonction_id":  f.id,
                "personnel_id": f.personnelle.id,
                "nom":          f.personnelle.nom,
                "prenom":       f.personnelle.prenom,
                "fonction":     f.nom,
                "service":      f.service.nom if f.service else "—",
                "superieurs": [
                    {
                        "login_id": s.id,
                        "nom":      s.personnelle.nom      if s.personnelle else "—",
                        "prenom":   s.personnelle.prenom   if s.personnelle else "—",
                        "role":     s.role.name            if s.role        else "—",
                    }
                    for s in f.superieurs.all()
                ]
            })

        # Liste des logins disponibles comme supérieurs (Chef, Admin, Super Admin, GP, RF)
        logins_disponibles = Login.objects.select_related(
            'personnelle', 'role'
        ).exclude(role__name='User')

        disponibles = [
            {
                "login_id": l.id,
                "nom":      l.personnelle.nom    if l.personnelle else "—",
                "prenom":   l.personnelle.prenom if l.personnelle else "—",
                "role":     l.role.name          if l.role        else "—",
            }
            for l in logins_disponibles
            if l.personnelle  # seulement ceux liés à un personnel
        ]

        return Response({
            "status":      "success",
            "personnels":  data,
            "disponibles": disponibles
        })

    def patch(self, request, fonction_id):
        """Modifier les supérieurs d'un personnel"""
        try:
            fonction       = Fonctions.objects.get(id=fonction_id)
            superieurs_ids = request.data.get('superieurs_ids', [])

            # Remplacer tous les supérieurs
            logins = Login.objects.filter(id__in=superieurs_ids)
            fonction.superieurs.set(logins)

            return Response({
                "status":  "success",
                "message": "Supérieurs mis à jour"
            })
        except Fonctions.DoesNotExist:
            return Response({
                "status":  "error",
                "message": "Fonction introuvable"
            }, status=status.HTTP_404_NOT_FOUND)