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
    """Requête de lecture pour la liste des étudiants avec pagination.
    
    Attributes:
        filtre_nom (Optional[str]): Filtre par nom ou prénom.
        page (int): Numéro de la page à récupérer.
        taille_page (int): Nombre d'éléments par page (défaut: 50).
    """
    filtre_nom: Optional[str] = None
    page: int = 1
    taille_page: int = 50

    # Injection via Handler/DI
    etudiant_repo = None

    def fetch(self) -> List:
        """Récupère la liste paginée des étudiants."""
        return self.etudiant_repo.list_all()
