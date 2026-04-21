from typing import List, Optional
from domain.entities.personnel import Personnel
from domain.repositories.i_personnel_repository import IPersonnelRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebasePersonnelRepository(IPersonnelRepository):
    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('personnel')

    def _to_dict(self, personnel: Personnel) -> dict:
        return {
            'nom': personnel._nom,
            'prenom': personnel._prenom,
            'email': personnel._email,
            'role': personnel._role,
            'user_id': personnel._user_id,
            'updated_at': personnel.updated_at
        }

    def _from_dict(self, doc_id: str, data: dict) -> Personnel:
        return Personnel(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            role=data['role'],
            user_id=data.get('user_id'),
            id=doc_id
        )

    def save(self, personnel: Personnel) -> None:
        self.collection.document(personnel.id).set(self._to_dict(personnel))

    def get_by_id(self, personnel_id: str) -> Optional[Personnel]:
        doc = self.collection.document(personnel_id).get()
        if doc.exists:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def get_by_email(self, email: str) -> Optional[Personnel]:
        docs = self.collection.where('email', '==', email).limit(1).stream()
        for doc in docs:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def list_all(self) -> List[Personnel]:
        docs = self.collection.stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def delete(self, personnel_id: str) -> None:
        self.collection.document(personnel_id).delete()
