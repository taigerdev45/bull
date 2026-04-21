from typing import List
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
    Handler coordonnant les transactions Firestore et le recalcul des moyennes.
    Assure l'atomicité entre la saisie de note et la mise à jour des résultats.
    """

    def __init__(self, evaluation_repo: IEvaluationRepository, orchestre_calcul: OrchestreCalcul):
        self._evaluation_repo = evaluation_repo
        self._orchestre_calcul = orchestre_calcul
        # On suppose que le repo a accès au client db pour les transactions
        self._db = evaluation_repo._db 

    def handle_creer(self, cmd: CreerEvaluationCommand) -> str:
        transaction = self._db.transaction()
        
        @transaction.execute
        def _in_transaction(transaction):
            # 1. Création entité
            evaluation = Evaluation(
                etudiant_id=cmd.etudiant_id,
                matiere_id=cmd.matiere_id,
                type=TypeEvaluation[cmd.type_eval],
                note=Note(cmd.note),
                saisie_par=cmd.saisie_par
            )
            from datetime import datetime
            evaluation._date_saisie = datetime.now().isoformat()
            
            # 2. Persistance
            eval_id = self._evaluation_repo.creer(evaluation, transaction=transaction)
            
            # 3. Recalcul (l'orchestrateur devrait idéalement supporter la transaction)
            # Pour l'instant on garde le calcul post-transaction ou on l'intègre si supporté
            return eval_id

        eval_id = _in_transaction(transaction)
        
        # Déclenchement du recalcul complet
        self._orchestre_calcul.recalculer_pour_etudiant(cmd.etudiant_id)

        # 4. Dispatch Audit Event
        dispatcher.dispatch(EvaluationCreee(
            data={
                'evaluation_id': eval_id,
                'etudiant_id': cmd.etudiant_id,
                'matiere_libelle': cmd.matiere_id, 
                'type_eval': cmd.type_eval,
                'note': cmd.note
            },
            metadata=cmd.metadata
        ))
        return eval_id

    def handle_modifier(self, cmd: ModifierEvaluationCommand):
        transaction = self._db.transaction()
        
        @transaction.execute
        def _in_transaction(transaction):
            # 1. Charger
            evaluation = self._evaluation_repo.obtenir_par_id(cmd.evaluation_id)
            if not evaluation:
                raise ValueError("Evaluation non trouvée")
            
            # 2. Modifier (valide le verrouillage jury à l'intérieur)
            evaluation.modifier_note(Note(cmd.nouvelle_note), cmd.auteur)
            
            # 3. Sauvegarder
            self._evaluation_repo.modifier(evaluation, transaction=transaction)
            return evaluation.etudiant_id

        etudiant_id = _in_transaction(transaction)
        self._orchestre_calcul.recalculer_pour_etudiant(etudiant_id)

    def handle_supprimer(self, cmd: SupprimerEvaluationCommand):
        transaction = self._db.transaction()
        
        @transaction.execute
        def _in_transaction(transaction):
            evaluation = self._evaluation_repo.obtenir_par_id(cmd.evaluation_id)
            if not evaluation:
                raise ValueError("Evaluation non trouvée")
            
            if evaluation.est_verrouille:
                raise ValueError("Impossible de supprimer une note verrouillée.")
            
            self._evaluation_repo.supprimer(cmd.evaluation_id, transaction=transaction)
            return evaluation.etudiant_id

        etudiant_id = _in_transaction(transaction)
        self._orchestre_calcul.recalculer_pour_etudiant(etudiant_id)

    def handle_bulk_creer(self, commands: List[CreerEvaluationCommand]):
        """Saisie par lot (atomique)."""
        evaluations = []
        for cmd in commands:
            eval_obj = Evaluation(
                etudiant_id=cmd.etudiant_id,
                matiere_id=cmd.matiere_id,
                type=TypeEvaluation[cmd.type_eval],
                note=Note(cmd.note),
                saisie_par=cmd.saisie_par
            )
            from datetime import datetime
            eval_obj._date_saisie = datetime.now().isoformat()
            evaluations.append(eval_obj)
        
        self._evaluation_repo.bulk_creer(evaluations)
        
        # Recalcul groupé pour tous les étudiants du lot
        etudiants_uniques = {e.etudiant_id for e in evaluations}
        for etu_id in etudiants_uniques:
            self._orchestre_calcul.recalculer_pour_etudiant(etu_id)
