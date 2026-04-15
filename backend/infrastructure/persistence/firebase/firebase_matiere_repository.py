from typing import List, Optional
from domain.entities.matiere import Matiere
from domain.value_objects.coefficient import Coefficient
from domain.repositories.i_matiere_repository import IMatiereRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebaseMatiereRepository(IMatiereRepository):
    """Implémentation du repository Matière avec Firestore."""

    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('matieres')

    def _to_dict(self, matiere: Matiere) -> dict:
        return {
            'libelle': matiere._libelle,
            'coefficient': matiere._coefficient.valeur,
            'credits': matiere._credits,
            'ue_id': matiere._ue_id,
            'enseignant_id': getattr(matiere, '_enseignant_id', None),
            'updated_at': matiere.updated_at
        }

    def _from_dict(self, doc_id: str, data: dict) -> Matiere:
        return Matiere(
            libelle=data['libelle'],
            coefficient=Coefficient(data['coefficient']),
            credits=data['credits'],
            ue_id=data['ue_id'],
            enseignant_id=data.get('enseignant_id'),
            id=doc_id
        )

    def save(self, matiere: Matiere) -> None:
        self.collection.document(matiere.id).set(self._to_dict(matiere))

    def get_by_id(self, id: str) -> Optional[Matiere]:
        doc = self.collection.document(id).get()
        if doc.exists:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def get_by_libelle(self, libelle: str) -> Optional[Matiere]:
        docs = self.collection.where('libelle', '==', libelle).limit(1).stream()
        for doc in docs:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def list_all(self) -> List[Matiere]:
        docs = self.collection.stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def get_by_ue(self, ue_id: str) -> List[Matiere]:
        """Récupère toutes les matières d'une UE."""
        docs = self.collection.where('ue_id', '==', ue_id).stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def get_by_enseignant(self, enseignant_id: str) -> List[Matiere]:
        """Récupère toutes les matières attribuées à un enseignant."""
        docs = self.collection.where('enseignant_id', '==', enseignant_id).stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def attribuer_enseignant(self, matiere_id: str, enseignant_id: str) -> None:
        """Assigne un enseignant à une matière."""
        self.collection.document(matiere_id).update({'enseignant_id': enseignant_id})

    def delete(self, id: str) -> None:
        self.collection.document(id).delete()
