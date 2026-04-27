import uuid
from datetime import datetime
from typing import Optional

class Notification:
    def __init__(
        self,
        destinataire_uid: str,
        titre: str,
        message: str,
        is_read: bool = False,
        type: str = 'INFO',
        created_at: Optional[datetime] = None,
        id: Optional[str] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.destinataire_uid = destinataire_uid
        self.titre = titre
        self.message = message
        self.is_read = is_read
        self.type = type
        self.created_at = created_at or datetime.now()

    def mark_as_read(self):
        self.is_read = True

    def to_dict(self):
        return {
            "id": self.id,
            "destinataire_uid": self.destinataire_uid,
            "titre": self.titre,
            "message": self.message,
            "is_read": self.is_read,
            "type": self.type,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
