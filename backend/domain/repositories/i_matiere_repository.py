from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.matiere import Matiere

class IMatiereRepository(ABC):
    """Interface Repository pour Matiere (DIP)"""

    @abstractmethod
    def save(self, matiere: Matiere) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Matiere]:
        pass

    @abstractmethod
    def get_by_libelle(self, libelle: str) -> Optional[Matiere]:
        """Recherche une matière par son libellé exact."""
        pass

    @abstractmethod
    def list_all(self) -> List[Matiere]:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass
