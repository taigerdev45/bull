from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.personnel import Personnel

class IPersonnelRepository(ABC):
    @abstractmethod
    def save(self, personnel: Personnel) -> None: pass
    @abstractmethod
    def get_by_id(self, personnel_id: str) -> Optional[Personnel]: pass
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Personnel]: pass
    @abstractmethod
    def list_all() -> List[Personnel]: pass
    @abstractmethod
    def delete(self, personnel_id: str) -> None: pass
