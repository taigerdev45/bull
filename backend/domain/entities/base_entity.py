from abc import ABC, abstractmethod
import uuid
from datetime import datetime

class BaseEntity(ABC):
    """Classe de base abstraite pour toutes les entités du domaine."""
    
    def __init__(self, id: str = None):
        self._id = id or str(uuid.uuid4())
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

    def update_timestamp(self):
        """Met à jour le timestamp de modification."""
        self._updated_at = datetime.now()

    @abstractmethod
    def valider(self):
        """Méthode de validation à implémenter par les entités concrètes."""
        pass

    def __eq__(self, other):
        if not isinstance(other, BaseEntity):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
