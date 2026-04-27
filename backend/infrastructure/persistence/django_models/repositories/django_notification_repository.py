from typing import List, Optional
from domain.entities.notification import Notification
from domain.repositories.i_notification_repository import INotificationRepository
from infrastructure.persistence.django_models.models import NotificationModel

class DjangoNotificationRepository(INotificationRepository):
    def save(self, notification: Notification) -> None:
        NotificationModel.objects.update_or_create(
            id=notification.id,
            defaults={
                'destinataire_uid': notification.destinataire_uid,
                'titre': notification.titre,
                'message': notification.message,
                'is_read': notification.is_read,
                'type': notification.type
            }
        )

    def get_by_id(self, id: str) -> Optional[Notification]:
        try:
            model = NotificationModel.objects.get(id=id)
            return self._to_entity(model)
        except NotificationModel.DoesNotExist:
            return None

    def list_by_user(self, user_uid: str, only_unread: bool = False) -> List[Notification]:
        query = NotificationModel.objects.filter(destinataire_uid=user_uid)
        if only_unread:
            query = query.filter(is_read=False)
        models = query.order_by('-created_at')
        return [self._to_entity(m) for m in models]

    def mark_as_read(self, notification_id: str) -> None:
        NotificationModel.objects.filter(id=notification_id).update(is_read=True)

    def delete(self, id: str) -> None:
        NotificationModel.objects.filter(id=id).delete()

    def _to_entity(self, model: NotificationModel) -> Notification:
        return Notification(
            id=model.id,
            destinataire_uid=model.destinataire_uid,
            titre=model.titre,
            message=model.message,
            is_read=model.is_read,
            type=model.type,
            created_at=model.created_at
        )
