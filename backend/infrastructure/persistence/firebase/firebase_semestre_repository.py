from typing import List, Optional
from domain.entities.semestre import Semestre
from domain.repositories.i_semestre_repository import ISemestreRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebaseSemestreRepository(ISemestreRepository):
    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('semestres')

    def _to_dict(self, semestre: Semestre) -> dict:
        return {
            'libelle': semestre.libelle,
            'annee_universitaire': semestre.annee_universitaire,
            'updated_at': semestre.updated_at
        }

    def _from_dict(self, doc_id: str, data: dict) -> Semestre:
        return Semestre(
            libelle=data['libelle'],
            annee_universitaire=data['annee_universitaire'],
            id=doc_id
        )

    def save(self, semestre: Semestre) -> None:
        self.collection.document(semestre.id).set(self._to_dict(semestre))

    def get_by_id(self, semestre_id: str) -> Optional[Semestre]:
        doc = self.collection.document(semestre_id).get()
        if doc.exists:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def list_all(self) -> List[Semestre]:
        docs = self.collection.stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def delete(self, semestre_id: str) -> None:
        self.collection.document(semestre_id).delete()
