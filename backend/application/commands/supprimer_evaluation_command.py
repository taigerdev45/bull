from dataclasses import dataclass
from .command import Command

@dataclass
class SupprimerEvaluationCommand(Command):
    """Données pour la suppression d'une évaluation."""
    evaluation_id: str
    auteur: str
    metadata: dict = None

    def executer(self) -> any:
        pass
