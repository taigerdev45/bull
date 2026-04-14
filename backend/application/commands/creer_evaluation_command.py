from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

class Command(ABC):
    """Interface de base pour toutes les commandes (Unit of Work)."""
    @abstractmethod
    def executer(self) -> any:
        pass

@dataclass
class CreerEvaluationCommand(Command):
    """Commande de création d'une évaluation avec recalcul automatique."""
    etudiant_id: str
    matiere_id: str
    type_eval: str
    note: float
    
    # Injection via Handler/DI
    evaluation_repo = None
    orchestre_calcul = None

    def executer(self) -> str:
        from domain.entities.evaluation import Evaluation, TypeEvaluation
        from domain.value_objects.note import Note
        
        # 1. Création de l'entité
        evaluation = Evaluation(
            etudiant_id=self.etudiant_id,
            matiere_id=self.matiere_id,
            type=TypeEvaluation[self.type_eval],
            note=Note(self.note)
        )
        
        # 2. Persistance
        self.evaluation_repo.creer(evaluation)
        
        # 3. Déclenchement du calcul en cascade (simulé ici via orchestrateur)
        # self.orchestre_calcul.recalculer_pour_etudiant(self.etudiant_id)
        
        return evaluation.id
