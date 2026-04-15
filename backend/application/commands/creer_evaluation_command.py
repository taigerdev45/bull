from dataclasses import dataclass
from .command import Command

@dataclass
class CreerEvaluationCommand(Command):
    """Données pour la création d'une évaluation."""
    etudiant_id: str
    matiere_id: str
    type_eval: str
    note: float
    saisie_par: str
    metadata: dict = None  # {ip, user_agent, user_email}

    def executer(self) -> any:
        # La logique est centralisée dans EvaluationCommandHandler
        pass
