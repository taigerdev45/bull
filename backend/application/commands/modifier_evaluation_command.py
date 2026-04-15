from dataclasses import dataclass
from .command import Command

@dataclass
class ModifierEvaluationCommand(Command):
    """Données pour la modification d'une évaluation."""
    evaluation_id: str
    nouvelle_note: float
    auteur: str
    metadata: dict = None

    def executer(self) -> any:
        pass
