from rest_framework.views import APIView
from rest_framework.response import Response

from api.models.conge.notification import Notification
from api.services.conge.notificationService import NotificationServices
from api.dto.conge.notificationDto import NotificationDto


class NotificationController(APIView):

    def get(self, request, id=None):
        if id:
            try:
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

    def delete(self, request, id):
        try:
            NotificationServices.delete(id)
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