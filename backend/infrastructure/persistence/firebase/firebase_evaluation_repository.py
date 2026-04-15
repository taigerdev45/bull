from typing import List, Optional
from google.cloud.firestore import FieldFilter

from domain.repositories.i_evaluation_repository import IEvaluationRepository
from domain.entities.evaluation import Evaluation
from .connection import FirebaseConnection

class FirebaseEvaluationRepository(IEvaluationRepository):
    """
    Implémentation concrète du repository avec Firebase.
    Peut être remplacé par PostgreSQL sans toucher au domaine.
    """
    
    COLLECTION = 'evaluations'
    
    def __init__(self, connection: FirebaseConnection = None):
        self._db = (connection or FirebaseConnection()).client
    
    def creer(self, evaluation: Evaluation, transaction=None) -> str:
        doc_ref = self._db.collection(self.COLLECTION).document()
        data = self._to_firestore(evaluation)
        if transaction:
            transaction.set(doc_ref, data)
        else:
            doc_ref.set(data)
        evaluation._id = doc_ref.id
        return doc_ref.id
    
    def bulk_creer(self, evaluations: List[Evaluation]) -> List[str]:
        batch = self._db.batch()
        ids = []
        for eval_obj in evaluations:
            doc_ref = self._db.collection(self.COLLECTION).document()
            batch.set(doc_ref, self._to_firestore(eval_obj))
            eval_obj._id = doc_ref.id
            ids.append(doc_ref.id)
        batch.commit()
        return ids
    
    def modifier(self, evaluation: Evaluation, transaction=None) -> None:
        if not evaluation.id:
            raise ValueError("Evaluation sans ID")
        
        doc_ref = self._db.collection(self.COLLECTION).document(evaluation.id)
        data = self._to_firestore(evaluation)
        if transaction:
            transaction.update(doc_ref, data)
        else:
            doc_ref.update(data)
    
    def obtenir_par_id(self, id: str) -> Optional[Evaluation]:
        doc = self._db.collection(self.COLLECTION).document(id).get()
        if doc.exists:
            eval_obj = self._from_firestore(doc)
            if eval_obj.est_supprime:
                return None
            return eval_obj
        return None

    def obtenir_par_etudiant(self, etudiant_id: str) -> List[Evaluation]:
        docs = self._db.collection(self.COLLECTION)\
            .where('etudiant_id', '==', etudiant_id)\
            .where('deleted_at', '==', None)\
            .stream()
        return [self._from_firestore(d) for d in docs]

    def obtenir_par_matiere(self, matiere_id: str) -> List[Evaluation]:
        docs = self._db.collection(self.COLLECTION)\
            .where('matiere_id', '==', matiere_id)\
            .where('deleted_at', '==', None)\
            .stream()
        return [self._from_firestore(d) for d in docs]

    def obtenir_par_etudiant_matiere(self, etudiant_id: str, 
                                      matiere_id: str) -> List[Evaluation]:
        docs = self._db.collection(self.COLLECTION)\
            .where('etudiant_id', '==', etudiant_id)\
            .where('matiere_id', '==', matiere_id)\
            .where('deleted_at', '==', None)\
            .stream()
        
        return [self._from_firestore(d) for d in docs]

    def supprimer(self, id: str, transaction=None) -> None:
        doc_ref = self._db.collection(self.COLLECTION).document(id)
        from datetime import datetime
        data = {'deleted_at': datetime.now().isoformat()}
        if transaction:
            transaction.update(doc_ref, data)
        else:
            doc_ref.update(data)
    
    def _to_firestore(self, evaluation: Evaluation) -> dict:
        return {
            'etudiant_id': evaluation.etudiant_id,
            'matiere_id': evaluation.matiere_id,
            'type': evaluation.type.value,
            'note': evaluation.note.valeur,
            'date_saisie': evaluation.date_saisie,
            'saisie_par': evaluation.saisie_par,
            'deleted_at': evaluation._deleted_at,
            'verrouille': evaluation._verrouille,
            'historique': evaluation._historique
        }
    
    def _from_firestore(self, doc) -> Evaluation:
        data = doc.to_dict()
        from domain.value_objects.note import Note
        from domain.entities.evaluation import TypeEvaluation
        
        eval_obj = Evaluation(
            id=doc.id,
            etudiant_id=data['etudiant_id'],
            matiere_id=data['matiere_id'],
            type=TypeEvaluation(data['type']),
            note=Note(data.get('note')),
            date_saisie=data.get('date_saisie'),
            saisie_par=data.get('saisie_par')
        )
        eval_obj._deleted_at = data.get('deleted_at')
        eval_obj._verrouille = data.get('verrouille', False)
        eval_obj._historique = data.get('historique', [])
        return eval_obj
