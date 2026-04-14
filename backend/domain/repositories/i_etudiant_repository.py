from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.etudiant import Etudiant

class IEtudiantRepository(ABC):
    """Interface pour le repository des Étudiants (DIP)."""
    
    @abstractmethod
    def save(self, etudiant: Etudiant) -> None:
        """Sauvegarde ou mjour un udiant."""
        pass

    @abstractmethod
    def get_by_id(self, etudiant_id: str) -> Optional[Etudiant]:
        """Rupe un udiant par son ID."""
        pass

    @abstractmethod
    def list_all(self) -> List[Etudiant]:
        """Liste tous les udiants."""
        pass

    @abstractmethod
    def delete(self, etudiant_id: str) -> None:
        """Supprime un udiant."""
        pass
