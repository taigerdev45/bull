from typing import List
from django.db import transaction
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from domain.services.orchestre_calcul import OrchestreCalcul
from domain.entities.evaluation import Evaluation, TypeEvaluation
from domain.value_objects.note import Note
from application.commands.creer_evaluation_command import CreerEvaluationCommand
from application.commands.modifier_evaluation_command import ModifierEvaluationCommand
from application.commands.supprimer_evaluation_command import SupprimerEvaluationCommand
from domain.events.evaluation_creee import EvaluationCreee
from domain.events.evaluation_modifiee import EvaluationModifiee
from domain.events.evaluation_supprimee import EvaluationSupprimee
from domain.events.event_dispatcher import dispatcher

class EvaluationCommandHandler:
    """
    Handler coordonnant les opérations sur les évaluations et le recalcul des moyennes.
    Utilise les transactions Django pour assurer l'intégrité des données.
    """

    def __init__(self, evaluation_repo: IEvaluationRepository, orchestre_calcul: OrchestreCalcul):
        self._evaluation_repo = evaluation_repo
        self._orchestre_calcul = orchestre_calcul

    def handle_creer(self, cmd: CreerEvaluationCommand) -> str:
        with transaction.atomic():
            # 1. Création entité
            evaluation = Evaluation(
                etudiant_id=cmd.etudiant_id,
                matiere_id=cmd.matiere_id,
                type=TypeEvaluation[cmd.type_eval],
                note=Note(cmd.note),
                saisie_par=cmd.saisie_par
            )
            
            # 2. Persistance
            eval_id = self._evaluation_repo.creer(evaluation)
            
            # 3. Recalcul
            self._orchestre_calcul.recalculer_pour_etudiant(cmd.etudiant_id)

            # 4. Dispatch Audit Event
            dispatcher.dispatch(EvaluationCreee(
                data={
                    'evaluation_id': eval_id,
                    'etudiant_id': cmd.etudiant_id,
                    'matiere_id': cmd.matiere_id, 
                    'type_eval': cmd.type_eval,
                    'note': cmd.note
                },
                metadata=cmd.metadata
            ))
            return eval_id

    def handle_modifier(self, cmd: ModifierEvaluationCommand):
        with transaction.atomic():
            # 1. Charger
            evaluation = self._evaluation_repo.obtenir_par_id(cmd.evaluation_id)
            if not evaluation:
                raise ValueError("Evaluation non trouvée")
            
            # 2. Modifier
            evaluation.modifier_note(Note(cmd.nouvelle_note), cmd.auteur)
            
            # 3. Sauvegarder
            self._evaluation_repo.modifier(evaluation)
            
            # 4. Recalcul
            self._orchestre_calcul.recalculer_pour_etudiant(evaluation.etudiant_id)

    def handle_supprimer(self, cmd: SupprimerEvaluationCommand):
        with transaction.atomic():
            evaluation = self._evaluation_repo.obtenir_par_id(cmd.evaluation_id)
            if not evaluation:
                raise ValueError("Evaluation non trouvée")
            
            if evaluation.est_verrouille:
                raise ValueError("Impossible de supprimer une note verrouillée.")
            
            self._evaluation_repo.supprimer(cmd.evaluation_id)
            
            # Recalcul
            self._orchestre_calcul.recalculer_pour_etudiant(evaluation.etudiant_id)

    def handle_bulk_creer(self, commands: List[CreerEvaluationCommand]):
        """Saisie par lot (atomique)."""
        with transaction.atomic():
            evaluations = []
            for cmd in commands:
                eval_obj = Evaluation(
                    etudiant_id=cmd.etudiant_id,
                    matiere_id=cmd.matiere_id,
                    type=TypeEvaluation[cmd.type_eval],
                    note=Note(cmd.note),
                    saisie_par=cmd.saisie_par
                )
                evaluations.append(eval_obj)
            
            self._evaluation_repo.bulk_creer(evaluations)
            
            # Recalcul groupé
            etudiants_uniques = {e.etudiant_id for e in evaluations}
            for etu_id in etudiants_uniques:
                self._orchestre_calcul.recalculer_pour_etudiant(etu_id)
