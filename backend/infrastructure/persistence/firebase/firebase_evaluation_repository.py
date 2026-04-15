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
    
    def creer(self, evaluation: Evaluation) -> str:
        doc_ref = self._db.collection(self.COLLECTION).document()
        doc_ref.set(self._to_firestore(evaluation))
        evaluation._id = doc_ref.id  # Met à jour l'entité
        return doc_ref.id
    
    def modifier(self, evaluation: Evaluation) -> None:
        if not evaluation.id:
            raise ValueError("Evaluation sans ID")
        
        self._db.collection(self.COLLECTION).document(
            evaluation.id
        ).update(self._to_firestore(evaluation))
    
    def obtenir_par_id(self, id: str) -> Optional[Evaluation]:
        doc = self._db.collection(self.COLLECTION).document(id).get()
        if doc.exists:
            return self._from_firestore(doc)
        return None

    def obtenir_par_etudiant(self, etudiant_id: str) -> List[Evaluation]:
        docs = self._db.collection(self.COLLECTION)\
            .where('etudiant_id', '==', etudiant_id)\
            .stream()
        return [self._from_firestore(d) for d in docs]

    def obtenir_par_etudiant_matiere(self, etudiant_id: str, 
                                      matiere_id: str) -> List[Evaluation]:
        docs = self._db.collection(self.COLLECTION)\
            .where('etudiant_id', '==', etudiant_id)\
            .where('matiere_id', '==', matiere_id)\
            .stream()
        
        return [self._from_firestore(d) for d in docs]

    def supprimer(self, id: str) -> None:
        self._db.collection(self.COLLECTION).document(id).delete()
    
    def _to_firestore(self, evaluation: Evaluation) -> dict:
        return {
            'etudiant_id': evaluation.etudiant_id,
            'matiere_id': evaluation.matiere_id,
            'type': evaluation.type.value,
            'note': evaluation.note.valeur,
            'date_saisie': evaluation.date_saisie,
            'saisie_par': evaluation.saisie_par
        }
    
    def _from_firestore(self, doc) -> Evaluation:
        data = doc.to_dict()
        from domain.value_objects.note import Note
        from domain.entities.evaluation import TypeEvaluation
        
        return Evaluation(
            identifiant=doc.id,
            etudiant_id=data['etudiant_id'],
            matiere_id=data['matiere_id'],
            type=TypeEvaluation(data['type']),
            note=Note(data.get('note')),
            date_saisie=data['date_saisie'],
            saisie_par=data['saisie_par']
        )
