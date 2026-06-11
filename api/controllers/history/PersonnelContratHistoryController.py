# =====================================================================
# CONTRÔLEUR DÉDIÉ POUR RÉCUPÉRER L'HISTORIQUE D'UN CONTRAT (React Front)
# =====================================================================

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer

class PersonnelContratHistoryController(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, personnel_id):
        """
        Endpoint accessible via : GET /api/fullpersonnelles/<personnel_id>/archive/
        """
        from django.db import connection

        query = """
            SELECT 
                h.id as history_id,
                h.history_date::text as history_date,
                '~' as history_type,
                h."NumeroContrat",
                h.salaire::text as salaire,
                h."dateDebut"::text as dateDebut,
                h."dateFin"::text as dateFin,
                h."periodeEssai",
                h.is_actif,
                f.nom as fonction_nom,
                s.nom as service_nom,
                tc."TypeContrat" as type_contrat_nom,
                mf.nom as financement_nom
            FROM public.api_contrathistory h
            LEFT JOIN public.api_fonctions f ON h.fonction_id = f.id
            LEFT JOIN public.api_services s ON h.service_id = s.id
            LEFT JOIN public.api_typecontrats tc ON h."typeContrat_id" = tc.id
            LEFT JOIN public.api_modefinancement mf ON h.financement_id = mf.id
            WHERE h.personnelle_id = %s
            ORDER BY h.history_date DESC
        """
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [personnel_id])
                columns = [col[0] for col in cursor.description]
                results = [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]
            return Response(results, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)