from typing import List, Optional
from domain.entities.evaluation import Evaluation, TypeEvaluation
from domain.value_objects.note import Note
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from ..django_models.models import EvaluationModel, EtudiantModel, MatiereModel

class SQLiteEvaluationRepository(IEvaluationRepository):
    """Implémentation du repository Evaluation utilisant l'ORM Django (SQLite/Turso)."""

    def creer(self, evaluation: Evaluation) -> str:
        etudiant_model = EtudiantModel.objects.get(id=evaluation.etudiant_id)
        matiere_model = MatiereModel.objects.get(id=evaluation.matiere_id)
        
        model = EvaluationModel.objects.create(
            id=evaluation.id,
            etudiant=etudiant_model,
            matiere=matiere_model,
            type=evaluation.type.name,
            note=evaluation.note.valeur
        )
        return model.id

    def bulk_creer(self, evaluations: List[Evaluation]) -> List[str]:
        ids = []
        for eval in evaluations:
            ids.append(self.creer(eval))
        return ids

    def modifier(self, evaluation: Evaluation) -> None:
        EvaluationModel.objects.filter(id=evaluation.id).update(
            note=evaluation.note.valeur,
            type=evaluation.type.name
        )

    def obtenir_par_id(self, id: str) -> Optional[Evaluation]:
        try:
            model = EvaluationModel.objects.get(id=id)
            return self._to_entity(model)
        except EvaluationModel.DoesNotExist:
            return None

    def obtenir_par_etudiant(self, etudiant_id: str) -> List[Evaluation]:
        models = EvaluationModel.objects.filter(etudiant_id=etudiant_id)
        return [self._to_entity(m) for m in models]

    def obtenir_par_matiere(self, matiere_id: str) -> List[Evaluation]:
        models = EvaluationModel.objects.filter(matiere_id=matiere_id)
        return [self._to_entity(m) for m in models]

    def obtenir_par_etudiant_matiere(self, etudiant_id: str, matiere_id: str) -> List[Evaluation]:
        models = EvaluationModel.objects.filter(etudiant_id=etudiant_id, matiere_id=matiere_id)
        return [self._to_entity(m) for m in models]

    def supprimer(self, id: str) -> None:
        EvaluationModel.objects.filter(id=id).delete()

    def _to_entity(self, model: EvaluationModel) -> Evaluation:
        return Evaluation(
            etudiant_id=model.etudiant.id,
            matiere_id=model.matiere.id,
            type_eval=TypeEvaluation[model.type],
            note=Note(model.note),
            id=model.id
        )
