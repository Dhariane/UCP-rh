from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.models.conge.conge import Conge
from api.models.conge.statut import Statut
from api.models.auth.login.loginModel import Login
from api.models.fonction.contrat import Contrat
from api.models.propos.personnelles import Personnelles
from api.models.propos.personnelles import Personnelles
from api.signal.conge_signal import envoi_notification_suivante, envoi_notification_refus


def get_etape_suivante(conge: Conge) -> str:
    """
    Calcule l'étape suivante selon le workflow.
    Règle : si le CN est le chef direct, on saute gp_rf.
    """
    ordre = ['passation', 'chef', 'gp_rf', 'cn', 'rh', 'termine']

    # Vérifier si on doit sauter gp_rf
    try:
        contrat = Contrat.objects.filter(
            personnelle=conge.personnel, is_actif=True
        ).first()
        if contrat and contrat.fonction and contrat.fonction.chef_direct:
            cn_est_chef = Login.objects.filter(
                personnelle__contrats__fonction=contrat.fonction.chef_direct,
                role__name='CN'
            ).exists()
            if cn_est_chef:
                ordre.remove('gp_rf')
    except Exception:
        pass

    try:
        idx = ordre.index(conge.etape_validation)
        return ordre[idx + 1] if idx + 1 < len(ordre) else 'termine'
    except ValueError:
        return 'termine'


class CongeValidationController(APIView):

    def post(self, request, id=None, conge_id=None):
        """
        Valider ou refuser un congé à l'étape courante.
        Body : { "decision": "approuve"|"refuse", "login_id": 12, "motif": "..." }
        """
        pk = id or conge_id
        try:
            decision = request.data.get('decision')
            motif    = request.data.get('motif', '')
            login_id = request.data.get('login_id')

            if decision not in ('approuve', 'refuse'):
                return Response({
                    "status": "error",
                    "message": "decision doit être 'approuve' ou 'refuse'"
                }, status=status.HTTP_400_BAD_REQUEST)

            conge       = get_object_or_404(Conge, id=pk)
            # ✅ Chercher par login_id ou personnel_id
            login_obj = Login.objects.filter(id=login_id).first()
            if not login_obj:
                personnel = Personnelles.objects.filter(id=login_id).first()
                if personnel:
                    login_obj = Login.objects.filter(personnelle=personnel).first()

            # ── REFUS ────────────────────────────────────────────────────────
            if decision == 'refuse':
                statut_refuse        = Statut.objects.get(code='refuse')
                conge.statut         = statut_refuse
                conge.etape_validation = 'termine'
                conge.validated_by   = login_obj
                conge.save()
                envoi_notification_refus(conge, login_obj)
                return Response({
                    "status":  "success",
                    "message": "Demande refusée",
                    "data":    {"etape_validation": "termine", "statut": "refuse"}
                })

            # ── APPROBATION ──────────────────────────────────────────────────
            # Cas spécial : étape passation → valider la passation de service
            if conge.etape_validation == 'passation':
                if conge.passation_service:
                    statut_valide = Statut.objects.get(id=2)
                    conge.passation_service.statut = statut_valide
                    conge.passation_service.save()

            prochaine_etape        = get_etape_suivante(conge)
            conge.etape_validation = prochaine_etape
            conge.validated_by     = login_obj

            # Approuvé définitivement quand on arrive à 'termine'
            if prochaine_etape == 'termine':
                statut_approuve = Statut.objects.get(code='approuve')
                conge.statut    = statut_approuve

            conge.save()
            envoi_notification_suivante(conge)

            return Response({
                "status":  "success",
                "message": f"Étape validée → {prochaine_etape}",
                "data": {
                    "etape_validation": prochaine_etape,
                    "statut": conge.statut.code if conge.statut else None
                }
            })

        except Statut.DoesNotExist as e:
            return Response({
                "status":  "error",
                "message": f"Statut introuvable : {e}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "status":  "error",
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, id=None, conge_id=None):
        """Historique des validations d'un congé"""
        pk = id or conge_id
        try:
            conge = Conge.objects.get(id=pk)
            validations = conge.validations.all()
            data = [
                {
                    "etape":    v.etape,
                    "decision": v.decision,
                    "valideur": (
                        f"{v.valideur.personnelle.prenom} {v.valideur.personnelle.nom}"
                        if v.valideur and v.valideur.personnelle else "—"
                    ),
                    "motif": v.motif,
                    "date":  v.date,
                }
                for v in validations
            ]
            return Response({"status": "success", "data": data})
        except Conge.DoesNotExist:
            return Response({
                "status": "error", "message": f"Congé introuvable (ID: {pk})"
            }, status=status.HTTP_404_NOT_FOUND)