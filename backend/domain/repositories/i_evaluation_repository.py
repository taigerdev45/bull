from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.evaluation import Evaluation

class IEvaluationRepository(ABC):
    """Interface pour le repository des Évaluations."""

    @abstractmethod
    def creer(self, evaluation: Evaluation) -> None:
        """Enregistre une nouvelle évaluation."""
        pass

    @abstractmethod
    def modifier(self, evaluation: Evaluation) -> None:
        """Met à jour une évaluation existante."""
        pass

    @abstractmethod
    def obtenir_par_id(self, evaluation_id: str) -> Optional[Evaluation]:
        """Récupère une évaluation par son ID."""
        pass

    @abstractmethod
    def obtenir_par_etudiant(self, etudiant_id: str) -> List[Evaluation]:
        """Récupère toutes les évaluations d'un étudiant."""
        pass

    @abstractmethod
    def obtenir_par_etudiant_matiere(self, etudiant_id: str, matiere_id: str) -> List[Evaluation]:
        """Récupère les évaluations d'un étudiant pour une matière donnée."""
        pass

    @abstractmethod
    def supprimer(self, evaluation_id: str) -> None:
        """Supprime une évaluation."""
        pass
