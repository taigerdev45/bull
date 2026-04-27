from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.notification import Notification

class INotificationRepository(ABC):
    @abstractmethod
    def save(self, notification: Notification) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Notification]:
        pass

    @abstractmethod
    def list_by_user(self, user_uid: str, only_unread: bool = False) -> List[Notification]:
        pass

    @abstractmethod
    def mark_as_read(self, notification_id: str) -> None:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass
