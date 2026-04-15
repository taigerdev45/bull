from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.absence import Absence

class IAbsenceRepository(ABC):
    """Interface pour le repository des absences (DIP)."""

    @abstractmethod
    def creer(self, absence: Absence) -> str:
        """Enregistre une nouvelle absence."""
        pass

    @abstractmethod
    def modifier(self, absence: Absence) -> None:
        """Met à jour une absence existante."""
        pass

    @abstractmethod
    def supprimer(self, absence_id: str) -> None:
        """Supprime une absence."""
        pass

    @abstractmethod
    def obtenir_par_id(self, absence_id: str) -> Optional[Absence]:
        """Récupère une absence par son ID."""
        pass

    @abstractmethod
    def obtenir_par_etudiant(self, etudiant_id: str) -> List[Absence]:
        """Récupère toutes les absences d'un étudiant."""
        pass

    @abstractmethod
    def obtenir_par_etudiant_matiere(self, etudiant_id: str, matiere_id: str) -> List[Absence]:
        """Récupère les absences d'un étudiant pour une matière spécifique."""
        pass

    @abstractmethod
    def calculer_total_heures(self, etudiant_id: str, matiere_id: str) -> int:
        """Calcule le nombre total d'heures d'absence pour un étudiant dans une matière."""
        pass
