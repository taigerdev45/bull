from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.ue import UE
from domain.entities.resultat import ResultatUE, ResultatSemestre, ResultatAnnuel

class IUERepository(ABC):
    """Interface pour le repository des Unités d'Enseignement."""
    @abstractmethod
    def save(self, ue: UE) -> None: pass
    @abstractmethod
    def get_by_id(self, ue_id: str) -> Optional[UE]: pass
    @abstractmethod
    def list_all(self) -> List[UE]: pass
