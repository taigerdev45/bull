from typing import List, Optional
from domain.entities.personnel import Personnel
from domain.repositories.i_personnel_repository import IPersonnelRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebasePersonnelRepository(IPersonnelRepository):
    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('utilisateurs')

    def _to_dict(self, personnel: Personnel) -> dict:
        return {
            'nom': personnel._nom,
            'prenom': personnel._prenom,
            'email': personnel._email,
            'numero_telephone': personnel._numero_telephone,
            'derniere_connexion': personnel._derniere_connexion,
            'role': personnel._role,
            'user_id': personnel._user_id,
            'updated_at': personnel.updated_at
        }

    def _from_dict(self, doc_id: str, data: dict) -> Personnel:
        return Personnel(
            nom=data.get('nom', ''),
            prenom=data.get('prenom', ''),
            email=data.get('email', ''),
            numero_telephone=data.get('numero_telephone'),
            derniere_connexion=data.get('derniere_connexion'),
            role=data.get('role', ''),
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
