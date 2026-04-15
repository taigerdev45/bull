from abc import ABC, abstractmethod
from typing import Any, Dict

class ICalculateur(ABC):
    """Interface pour tous les calculateurs"""
    
    @abstractmethod
    def calculer(self, contexte: Dict[str, Any]) -> Any:
        """Calcule un résultat à partir d'un contexte"""
        pass
    
    @abstractmethod
    def peut_calculer(self, contexte: Dict[str, Any]) -> bool:
        """Vérifie si le calcul est possible avec les données fournies"""
        pass
