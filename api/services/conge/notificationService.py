from django.utils import timezone
from api.models.conge.notification import Notification


class NotificationServices:

    @staticmethod
    def getAll(destinataire_id):
        return Notification.objects.filter(
            destinataire_id=destinataire_id
        )

    @staticmethod
    def getNonLues(destinataire_id):
        return Notification.objects.filter(
            destinataire_id=destinataire_id,
            lu=False
        )

    @staticmethod
    def countNonLues(destinataire_id) -> int:
        return Notification.objects.filter(
            destinataire_id=destinataire_id,
            lu=False
        ).count()

    @staticmethod
    def getById(id) -> Notification:
        return Notification.objects.get(id=id)

    @staticmethod
    def marquerLu(id) -> Notification:
        notif = Notification.objects.get(id=id)
        notif.marquer_lu()
        return notif

    @staticmethod
    def marquerToutLu(destinataire_id) -> int:
        updated = Notification.objects.filter(
            destinataire_id=destinataire_id,
            lu=False
        ).update(lu=True, date_lecture=timezone.now())
        return updated

    @staticmethod
    def delete(id):
        notif = Notification.objects.get(id=id)
        notif.delete()