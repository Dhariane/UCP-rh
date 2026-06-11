from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.models.conge.conge import Conge
from api.models.conge.statut import Statut
from api.models.conge.validationConge import ValidationConge
from api.models.auth.login.loginModel import Login
from api.models.propos.personnelles import Personnelles
from api.models.admin.loginadModel import Loginadmin
from api.signal.conge_signal import envoi_notification_suivante, envoi_notification_refus


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def get_etape_suivante(conge: Conge) -> str:
    from api.models.fonction.contrat import Contrat
    ordre = ['passation', 'chef', 'gp_pf', 'cn', 'rh', 'termine']

    try:
        contrat = Contrat.objects.filter(
            personnelle=conge.personnel, is_actif=True
        ).first()
        if contrat and contrat.fonction and contrat.fonction.chef_direct:
            cn_est_chef = Login.objects.filter(
                personnelle__contrats__fonction=contrat.fonction.chef_direct,
                personnelle__contrats__is_actif=True,
                role__name='CN'
            ).exists()
            if cn_est_chef and 'gp_pf' in ordre:
                ordre.remove('gp_pf')
    except Exception:
        pass

    try:
        idx = ordre.index(conge.etape_validation)
        return ordre[idx + 1] if idx + 1 < len(ordre) else 'termine'
    except ValueError:
        return 'termine'


def get_login_from_id(login_id):
    """Retourne (login_obj, is_admin)"""
    if not login_id:
        return None, False

    login = Login.objects.filter(id=login_id).first()
    if login:
        return login, False

    personnel = Personnelles.objects.filter(id=login_id).first()
    if personnel:
        login = Login.objects.filter(personnelle=personnel).first()
        if login:
            return login, False

    admin = Loginadmin.objects.filter(id=login_id).first()
    if admin:
        return None, True

    return None, False


def _sauvegarder_validation(conge, etape, decision, login_obj, motif):
    """Sauvegarde l'historique de validation avec motif."""
    try:
        ValidationConge.objects.create(
            conge=conge,
            etape=etape,
            decision=decision,
            valideur=login_obj,
            motif=motif or None
        )
    except Exception as e:
        print(f"[VALIDATION] Erreur sauvegarde : {e}")


# ─────────────────────────────────────────────
# CONTROLLER
# ─────────────────────────────────────────────

class CongeValidationController(APIView):

    def post(self, request, id=None, conge_id=None):
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

            conge = get_object_or_404(Conge, id=pk)
            login_obj, is_admin = get_login_from_id(login_id)

            # ── REFUS ──────────────────────────────────────────────
            if decision == 'refuse':
                etape_courante = conge.etape_validation  # ✅ avant modification
                conge.statut           = Statut.objects.get(id=3)
                conge.etape_validation = 'termine'
                conge.validated_by     = login_obj
                conge.save()

                _sauvegarder_validation(conge, etape_courante, 'refuse', login_obj, motif)
                envoi_notification_refus(conge, login_obj, motif)

                return Response({
                    "status":  "success",
                    "message": "Demande refusée",
                    "data":    {"etape_validation": "termine", "statut": "Refusé"}
                })

            # ── APPROBATION ────────────────────────────────────────
            etape_courante = conge.etape_validation  # ✅ avant modification

            if conge.etape_validation == 'passation':
                if conge.passation_service:
                    conge.passation_service.statut = Statut.objects.get(id=2)
                    conge.passation_service.save()

            prochaine_etape        = get_etape_suivante(conge)
            conge.etape_validation = prochaine_etape
            conge.validated_by     = login_obj

            if prochaine_etape == 'termine':
                conge.statut = Statut.objects.get(id=2)

            conge.save()

            _sauvegarder_validation(conge, etape_courante, 'approuve', login_obj, motif)
            envoi_notification_suivante(conge)

            return Response({
                "status":  "success",
                "message": f"Étape validée → {prochaine_etape}",
                "data": {
                    "etape_validation": prochaine_etape,
                    "statut": conge.statut.statut
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
                    "date":  str(v.date),
                }
                for v in validations
            ]
            return Response({"status": "success", "data": data})
        except Conge.DoesNotExist:
            return Response({
                "status":  "error",
                "message": f"Congé introuvable (ID: {pk})"
            }, status=status.HTTP_404_NOT_FOUND)