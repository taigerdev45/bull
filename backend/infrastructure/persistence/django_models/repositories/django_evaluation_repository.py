from typing import List, Optional
from domain.entities.evaluation import Evaluation, TypeEvaluation
from domain.value_objects.note import Note
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from infrastructure.persistence.django_models.models import EvaluationModel, EtudiantModel, MatiereModel

class DjangoEvaluationRepository(IEvaluationRepository):
    def save(self, evaluation: Evaluation) -> None:
        etudiant = EtudiantModel.objects.get(id=evaluation.etudiant_id)
        matiere = MatiereModel.objects.get(id=evaluation.matiere_id)
        
        EvaluationModel.objects.update_or_create(
            id=evaluation.id,
            defaults={
                'etudiant': etudiant,
                'matiere': matiere,
                'type': evaluation.type.name,
                'note': evaluation.note_valeur
            }
        )

    def get_by_id(self, id: str) -> Optional[Evaluation]:
        try:
            model = EvaluationModel.objects.get(id=id)
            return self._to_entity(model)
        except EvaluationModel.DoesNotExist:
            return None

    def list_by_etudiant(self, etudiant_id: str) -> List[Evaluation]:
        models = EvaluationModel.objects.filter(etudiant_id=etudiant_id)
        return [self._to_entity(m) for m in models]

    def list_by_matiere(self, matiere_id: str) -> List[Evaluation]:
        models = EvaluationModel.objects.filter(matiere_id=matiere_id)
        return [self._to_entity(m) for m in models]

    def list_by_etudiant_matiere(self, etudiant_id: str, matiere_id: str) -> List[Evaluation]:
        models = EvaluationModel.objects.filter(etudiant_id=etudiant_id, matiere_id=matiere_id)
        return [self._to_entity(m) for m in models]

    def delete(self, id: str) -> None:
        EvaluationModel.objects.filter(id=id).delete()

    def _to_entity(self, model: EvaluationModel) -> Evaluation:
        return Evaluation(
            etudiant_id=model.etudiant.id,
            matiere_id=model.matiere.id,
            type=TypeEvaluation[model.type],
            note=Note(model.note),
            id=model.id
        )
