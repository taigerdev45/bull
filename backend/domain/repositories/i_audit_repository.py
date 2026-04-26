from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class IAuditRepository(ABC):
    @abstractmethod
    def save(self, log_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def search_by_etudiant(self, etudiant_id: str, action: Optional[str] = None, 
                           date_debut: Optional[str] = None, date_fin: Optional[str] = None) -> List[Dict]:
        pass

    @abstractmethod
    def get_all(self, filtres: Optional[Dict] = None) -> List[Dict]:
        pass
