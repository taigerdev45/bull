from typing import List, Optional
from domain.entities.enseignant import Enseignant
from domain.repositories.i_enseignant_repository import IEnseignantRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebaseEnseignantRepository(IEnseignantRepository):
    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('enseignants')

    def _to_dict(self, enseignant: Enseignant) -> dict:
        return {
            'nom': enseignant._nom,
            'prenom': enseignant._prenom,
            'email': enseignant._email,
            'matricule': enseignant._matricule,
            'user_id': enseignant._user_id,
            'updated_at': enseignant.updated_at
        }

    def _from_dict(self, doc_id: str, data: dict) -> Enseignant:
        return Enseignant(
            nom=data['nom'],
            prenom=data['prenom'],
            email=data['email'],
            matricule=data.get('matricule', ''),
            user_id=data.get('user_id'),
            id=doc_id
        )

    def save(self, enseignant: Enseignant) -> None:
        self.collection.document(enseignant.id).set(self._to_dict(enseignant))

    def get_by_id(self, enseignant_id: str) -> Optional[Enseignant]:
        doc = self.collection.document(enseignant_id).get()
        if doc.exists:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def get_by_matricule(self, matricule: str) -> Optional[Enseignant]:
        docs = self.collection.where('matricule', '==', matricule).limit(1).stream()
        for doc in docs:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def list_all(self) -> List[Enseignant]:
        docs = self.collection.stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def delete(self, enseignant_id: str) -> None:
        self.collection.document(enseignant_id).delete()
