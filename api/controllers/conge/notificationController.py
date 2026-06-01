from rest_framework.views import APIView
from rest_framework.response import Response
<<<<<<< HEAD
from rest_framework import status
from api.models.conge.notification import Notification
from api.models.auth.login.loginModel import Login
from api.models.propos.personnelles import Personnelles
=======

from api.models.conge.notification import Notification
>>>>>>> 0a11ed57 (validation congé)
from api.services.conge.notificationService import NotificationServices
from api.dto.conge.notificationDto import NotificationDto


<<<<<<< HEAD
def get_login(login_id):
    """Cherche par login_id ou personnel_id"""
    login = Login.objects.filter(id=login_id).first()
    if not login:
        p = Personnelles.objects.filter(id=login_id).first()
        if p:
            login = Login.objects.filter(personnelle=p).first()
    return login


=======
>>>>>>> 0a11ed57 (validation congé)
class NotificationController(APIView):

    def get(self, request, id=None):
        if id:
            try:
<<<<<<< HEAD
                notif = NotificationServices.getById(id)
                return Response({"status": "success", "data": NotificationDto(notif).data})
            except Notification.DoesNotExist:
                return Response({"status": "error", "message": "Introuvable"}, status=404)

        # ✅ Filtrer par login_id
        login_id = request.query_params.get('login_id')
        if not login_id:
            return Response({"status": "error", "message": "login_id requis"}, status=400)

        login = get_login(login_id)
        if not login:
            return Response({"status": "success", "data": [], "total": 0})

        notifs = Notification.objects.filter(
            destinataire=login
        ).order_by('-date_creation')

        serializer = NotificationDto(notifs, many=True)
        return Response({
            "status": "success",
            "total": notifs.count(),
            "results": serializer.data
        })
=======
                obj = NotificationServices.getById(id)
                return Response({
                    "status": "success",
                    "data": NotificationDto(obj).data
                }, status=200)
            except Notification.DoesNotExist:
                return Response({
                    "status": "error",
                    "message": "Notification non trouvée"
                }, status=404)
        else:
            login_id  = request.user.id
            non_lues  = request.query_params.get('non_lues')

            if non_lues == '1':
                data = NotificationServices.getNonLues(login_id)
            else:
                data = NotificationServices.getAll(login_id)

            return Response({
                "status": "success",
                "data": NotificationDto(data, many=True).data
            }, status=200)
>>>>>>> 0a11ed57 (validation congé)

    def delete(self, request, id):
        try:
            NotificationServices.delete(id)
<<<<<<< HEAD
            return Response({"status": "success"}, status=204)
        except Notification.DoesNotExist:
            return Response({"status": "error"}, status=404)


class NotificationNonLuesCountController(APIView):
    def get(self, request):
        login_id = request.query_params.get('login_id')
        if not login_id:
            return Response({"count": 0})
        login = get_login(login_id)
        if not login:
            return Response({"count": 0})
        count = Notification.objects.filter(
            destinataire=login, lu=False
        ).count()
        return Response({"count": count})


class NotificationMarquerLuController(APIView):
    def patch(self, request, id):
        try:
            notif = NotificationServices.marquerLu(id)
            return Response({"status": "success", "data": NotificationDto(notif).data})
        except Notification.DoesNotExist:
            return Response({"status": "error"}, status=404)


class NotificationToutLireController(APIView):
    def patch(self, request):
        login_id = request.query_params.get('login_id')
        if not login_id:
            return Response({"status": "error", "message": "login_id requis"}, status=400)
        login = get_login(login_id)
        if not login:
            return Response({"status": "error"}, status=404)
        updated = NotificationServices.marquerToutLu(login.id)
        return Response({"status": "success", "updated": updated})
=======
            return Response({
                "status": "success",
                "message": "Supprimée avec succès"
            }, status=200)
        except Notification.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Notification non trouvée"
            }, status=404)


class NotificationNonLuesCountController(APIView):
    """
    GET /api/notifications/non-lues/count/
    Retourne le nombre de notifications non lues.
    """

    def get(self, request):
        count = NotificationServices.countNonLues(request.user.id)
        return Response({
            "status": "success",
            "data": {"count": count}
        }, status=200)


class NotificationMarquerLuController(APIView):
    """
    PATCH /api/notifications/<id>/lire/
    Marque une notification comme lue.
    """

    def patch(self, request, id):
        try:
            obj = NotificationServices.marquerLu(id)
            return Response({
                "status": "success",
                "data": NotificationDto(obj).data
            }, status=200)
        except Notification.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Notification non trouvée"
            }, status=404)


class NotificationToutLireController(APIView):
    """
    PATCH /api/notifications/tout-lire/
    Marque toutes les notifications comme lues.
    """

    def patch(self, request):
        updated = NotificationServices.marquerToutLu(request.user.id)
        return Response({
            "status": "success",
            "data": {"marked_read": updated}
        }, status=200)
>>>>>>> 0a11ed57 (validation congé)
