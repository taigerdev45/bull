from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.ue import UE
from domain.entities.resultat import ResultatUE, ResultatSemestre, ResultatAnnuel

class IUE_Repository(ABC):
    """Interface pour le repository des Unités d'Enseignement."""
    @abstractmethod
    def save(self, ue: UE) -> None: pass
    @abstractmethod
    def get_by_id(self, ue_id: str) -> Optional[UE]: pass
    @abstractmethod
    def list_all(self) -> List[UE]: pass

class IResultatRepository(ABC):
    """Interface pour le repository des Résultats calculés."""
    @abstractmethod
    def save_ue(self, resultat: ResultatUE) -> None: pass
    @abstractmethod
    def save_semestre(self, resultat: ResultatSemestre) -> None: pass
    @abstractmethod
    def save_annuel(self, resultat: ResultatAnnuel) -> None: pass
    @abstractmethod
    def get_par_etudiant(self, etudiant_id: str) -> List[ResultatUE]: pass
