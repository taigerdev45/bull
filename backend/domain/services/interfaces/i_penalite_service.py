from abc import ABC, abstractmethod

class IPenaliteService(ABC):
    """Interface pour le service de calcul des pénalités."""
    
    @abstractmethod
    def calculer(self, etudiant_id: str, matiere_id: str) -> float:
        """Calcule le montant de la pénalité pour un étudiant dans une matière."""
        pass
