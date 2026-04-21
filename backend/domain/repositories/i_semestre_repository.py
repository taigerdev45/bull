from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.semestre import Semestre

class ISemestreRepository(ABC):
    @abstractmethod
    def save(self, semestre: Semestre) -> None: pass
    @abstractmethod
    def get_by_id(self, semestre_id: str) -> Optional[Semestre]: pass
    @abstractmethod
    def list_all(self) -> List[Semestre]: pass
    @abstractmethod
    def delete(self, semestre_id: str) -> None: pass
