from typing import List, Optional
import uuid
from domain.entities.evaluation import Evaluation, TypeEvaluation
from domain.value_objects.note import Note
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from infrastructure.persistence.django_models.models import EvaluationModel, EtudiantModel, MatiereModel

class DjangoEvaluationRepository(IEvaluationRepository):
    def creer(self, evaluation: Evaluation) -> str:
        etudiant = EtudiantModel.objects.get(id=evaluation.etudiant_id)
        matiere = MatiereModel.objects.get(id=evaluation.matiere_id)
        
        # On utilise l'ID existant ou on en génère un nouveau
        eval_id = evaluation.id or str(uuid.uuid4())
        
        model = EvaluationModel.objects.create(
            id=eval_id,
            etudiant=etudiant,
            matiere=matiere,
            type=evaluation.type.name,
            note=evaluation.note_valeur
        )
        return model.id

    def bulk_creer(self, evaluations: List[Evaluation]) -> List[str]:
        ids = []
        for eval_obj in evaluations:
            ids.append(self.creer(eval_obj))
        return ids

    def modifier(self, evaluation: Evaluation) -> None:
        EvaluationModel.objects.filter(id=evaluation.id).update(
            note=evaluation.note_valeur,
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

    def obtenir_tout(self) -> List[Evaluation]:
        models = EvaluationModel.objects.all()
        return [self._to_entity(m) for m in models]

    def _to_entity(self, model: EvaluationModel) -> Evaluation:
        return Evaluation(
            etudiant_id=model.etudiant.id,
            matiere_id=model.matiere.id,
            type=TypeEvaluation[model.type],
            note=Note(model.note),
            id=model.id
        )
