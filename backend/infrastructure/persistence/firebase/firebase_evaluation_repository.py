from typing import List, Optional
from domain.entities.evaluation import Evaluation, TypeEvaluation
from domain.value_objects.note import Note
from domain.repositories.i_evaluation_repository import IEvaluationRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebaseEvaluationRepository(IEvaluationRepository):
    """Implémentation du repository Évaluation avec Firestore."""

    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('evaluations')

    def _to_dict(self, evaluation: Evaluation) -> dict:
        """Convertit une Entité en dictionnaire Firestore."""
        return {
            'etudiant_id': evaluation._etudiant_id,
            'matiere_id': evaluation._matiere_id,
            'type': evaluation._type.name,
            'note': evaluation._note.valeur,
            'updated_at': evaluation.updated_at
        }

    def _from_dict(self, doc_id: str, data: dict) -> Evaluation:
        """Convertit un dictionnaire Firestore en Entité."""
        return Evaluation(
            etudiant_id=data['etudiant_id'],
            matiere_id=data['matiere_id'],
            type=TypeEvaluation[data['type']],
            note=Note(data['note']),
            id=doc_id
        )

    def creer(self, evaluation: Evaluation) -> None:
        self.collection.document(evaluation.id).set(self._to_dict(evaluation))

    def modifier(self, evaluation: Evaluation) -> None:
        self.collection.document(evaluation.id).update(self._to_dict(evaluation))

    def obtenir_par_id(self, evaluation_id: str) -> Optional[Evaluation]:
        doc = self.collection.document(evaluation_id).get()
        if doc.exists:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def obtenir_par_etudiant(self, etudiant_id: str) -> List[Evaluation]:
        docs = self.collection.where('etudiant_id', '==', etudiant_id).stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def obtenir_par_etudiant_matiere(self, etudiant_id: str, matiere_id: str) -> List[Evaluation]:
        docs = self.collection.where('etudiant_id', '==', etudiant_id)\
                             .where('matiere_id', '==', matiere_id).stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def supprimer(self, evaluation_id: str) -> None:
        self.collection.document(evaluation_id).delete()
