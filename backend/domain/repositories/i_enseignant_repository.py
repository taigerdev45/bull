from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.enseignant import Enseignant

class IEnseignantRepository(ABC):
    @abstractmethod
    def save(self, enseignant: Enseignant) -> None: pass
    @abstractmethod
    def get_by_id(self, enseignant_id: str) -> Optional[Enseignant]: pass
    @abstractmethod
    def list_all(self) -> List[Enseignant]: pass
    @abstractmethod
    def delete(self, enseignant_id: str) -> None: pass
    @abstractmethod
    def get_by_matricule(self, matricule: str) -> Optional[Enseignant]: pass
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> Optional[Enseignant]: pass
