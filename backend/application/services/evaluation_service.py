from typing import List
from application.commands.creer_evaluation_command import CreerEvaluationCommand
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from domain.services.orchestre_calcul import OrchestreCalcul

class EvaluationService:
    """Façade applicative pour la gestion des notes et évaluations."""

    def __init__(self, evaluation_repo: IEvaluationRepository, orchestrateur: OrchestreCalcul):
        self.evaluation_repo = evaluation_repo
        self.orchestrateur = orchestrateur

    def saisir_note(self, etudiant_id: str, matiere_id: str, type_eval: str, note: float) -> str:
        """Exécute la commande de création d'une note."""
        command = CreerEvaluationCommand(etudiant_id, matiere_id, type_eval, note)
        command.evaluation_repo = self.evaluation_repo
        command.orchestre_calcul = self.orchestrateur
        return command.executer()
