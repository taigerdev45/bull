from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

class Query(ABC):
    """Interface de base pour toutes les requêtes de lecture."""
    @abstractmethod
    def fetch(self) -> any:
        pass

@dataclass
class ListerEtudiantsQuery(Query):
    """Requête de lecture pour la liste des étudiants avec pagination."""
    filtre_nom: Optional[str] = None
    page: int = 1
    taille_page: int = 20

    # Injection via Handler/DI
    etudiant_repo = None

    def fetch(self) -> List:
        # Logique de lecture directe via repository
        return self.etudiant_repo.list_all()
