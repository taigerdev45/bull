from typing import List, Optional
from domain.entities.etudiant import Etudiant
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection
from datetime import date

class FirebaseEtudiantRepository(IEtudiantRepository):
    """Implémentation du repository Étudiant avec Firestore."""

    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('etudiants')

    def _to_dict(self, etudiant: Etudiant) -> dict:
        return {
            'nom': etudiant._nom,
            'prenom': etudiant._prenom,
            'matricule': etudiant._matricule,
            'date_naissance': etudiant._date_naissance.isoformat() if etudiant._date_naissance else None,
            'updated_at': etudiant.updated_at
        }

    def _from_dict(self, doc_id: str, data: dict) -> Etudiant:
        return Etudiant(
            nom=data['nom'],
            prenom=data['prenom'],
            matricule=data['matricule'],
            date_naissance=date.fromisoformat(data['date_naissance']) if data.get('date_naissance') else None,
            id=doc_id
        )

    def save(self, etudiant: Etudiant) -> None:
        self.collection.document(etudiant.id).set(self._to_dict(etudiant))

    def get_by_id(self, etudiant_id: str) -> Optional[Etudiant]:
        doc = self.collection.document(etudiant_id).get()
        if doc.exists:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def get_by_matricule(self, matricule: str) -> Optional[Etudiant]:
        docs = self.collection.where('matricule', '==', matricule).limit(1).stream()
        for doc in docs:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def list_all(self) -> List[Etudiant]:
        docs = self.collection.stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def delete(self, etudiant_id: str) -> None:
        self.collection.document(etudiant_id).delete()
