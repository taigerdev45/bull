from typing import List, Optional
from domain.entities.ue import UE
from domain.repositories.i_ue_repository import IUERepository
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebaseUERepository(IUERepository):
    """Implémentation du repository UE avec Firestore."""

    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('ues')

    def _to_dict(self, ue: UE) -> dict:
        return {
            'code': ue.code,
            'libelle': ue.libelle,
            'credits': ue.credits,
            'semestre': ue.semestre,
            'updated_at': ue.updated_at
        }

    def _from_dict(self, doc_id: str, data: dict) -> UE:
        return UE(
            code=data['code'],
            libelle=data['libelle'],
            credits=data['credits'],
            semestre=data['semestre'],
            id=doc_id
        )

    def save(self, ue: UE) -> None:
        self.collection.document(ue.code).set(self._to_dict(ue))

    def get_by_id(self, id: str) -> Optional[UE]:
        doc = self.collection.document(id).get()
        if doc.exists:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def get_by_semestre(self, semestre: int) -> List[UE]:
        """Récupère toutes les UEs d'un semestre."""
        docs = self.collection.where('semestre', '==', semestre).stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def list_all(self) -> List[UE]:
        docs = self.collection.stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def delete(self, id: str) -> None:
        self.collection.document(id).delete()
