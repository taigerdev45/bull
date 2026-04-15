from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.evaluation import Evaluation

class IEvaluationRepository(ABC):
    """Interface Repository pour Evaluation (DIP)"""
    
    @abstractmethod
    def creer(self, evaluation: Evaluation) -> str:
        pass
    
    @abstractmethod
    def modifier(self, evaluation: Evaluation) -> None:
        pass
    
    @abstractmethod
    def obtenir_par_id(self, id: str) -> Optional[Evaluation]:
        pass
    
    @abstractmethod
    def obtenir_par_etudiant(self, etudiant_id: str) -> List[Evaluation]:
        pass
    
    @abstractmethod
    def obtenir_par_etudiant_matiere(self, etudiant_id: str, 
                                      matiere_id: str) -> List[Evaluation]:
        pass
    
    @abstractmethod
    def supprimer(self, id: str) -> None:
        pass
