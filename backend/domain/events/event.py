from datetime import datetime
from uuid import uuid4
from abc import ABC

class Event(ABC):
    """Classe de base pour tous les événements de domaine."""
    def __init__(self, data: dict, metadata: dict = None):
        self.event_id = str(uuid4())
        self.timestamp = datetime.now()
        self.data = data
        self.metadata = metadata or {}

    def to_dict(self):
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp.isoformat(),
            'data': self.data,
            'metadata': self.metadata
        }
