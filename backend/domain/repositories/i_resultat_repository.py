from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.resultat import ResultatUE, ResultatSemestre, ResultatAnnuel

class IResultatRepository(ABC):
    """Interface pour le repository des Résultats calculés."""

    @abstractmethod
    def save_ue(self, resultat: ResultatUE) -> None:
        """Sauvegarde un résultat d'UE."""
        pass

    @abstractmethod
    def save_semestre(self, resultat: ResultatSemestre) -> None:
        """Sauvegarde un résultat de semestre."""
        pass

    @abstractmethod
    def save_annuel(self, resultat: ResultatAnnuel) -> None:
        """Sauvegarde un résultat annuel."""
        pass

    @abstractmethod
    def get_par_etudiant_semestre(self, etudiant_id: str, semestre: int) -> Optional[ResultatSemestre]:
        """Récupère le résultat d'un semestre pour un étudiant donné."""
        pass

    @abstractmethod
    def get_par_etudiant_annuel(self, etudiant_id: str) -> Optional[ResultatAnnuel]:
        """Récupère le résultat annuel pour un étudiant donné."""
        pass

    @abstractmethod
    def obtenir_ue_details(self, etudiant_id: str, semestre: int) -> List[ResultatUE]:
        """Récupère la liste des résultats d'UE pour un semestre donné."""
        pass
