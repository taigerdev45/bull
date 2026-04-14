from abc import ABC, abstractmethod
from typing import Any

class ICalculateur(ABC):
    """Interface pour les stratégies de calcul métier."""
    
    @abstractmethod
    def calculer(self, data: Any) -> Any:
        """Exécute le calcul sur les données fournies."""
        pass

    @abstractmethod
    def peut_calculer(self, data: Any) -> bool:
        """Vérifie si le calculateur peut traiter ces données."""
        pass

class IValidateur(ABC):
    """Interface pour les stratégies de validation."""
    
    @abstractmethod
    def valider(self, data: Any) -> Any:
        """Valide les données et retourne un résultat de validation."""
        pass
