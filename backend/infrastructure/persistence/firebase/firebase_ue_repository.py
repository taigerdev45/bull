from typing import List, Optional, Any
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
            'semestre_id': int(ue._semestre_id) if str(ue._semestre_id).isdigit() else ue._semestre_id,
            'updated_at': ue.updated_at
        }

    def _from_dict(self, doc_id: str, data: dict) -> UE:
        # On essaie de récupérer semestre_id ou semestre (legacy)
        s_id = data.get('semestre_id') or data.get('semestre')
        # Conversion en int si possible
        if s_id and str(s_id).isdigit():
            s_id = int(s_id)
        elif s_id and "Semestre" in str(s_id):
            # Extraction du chiffre pour le libellé "Semestre X"
            import re
            match = re.search(r'\d+', str(s_id))
            if match:
                s_id = int(match.group())

        return UE(
            code=data['code'],
            libelle=data['libelle'],
            credits=data['credits'],
            semestre_id=s_id,
            id=doc_id
        )

    def save(self, ue: UE) -> None:
        self.collection.document(ue.code).set(self._to_dict(ue))

    def get_by_id(self, id: str) -> Optional[UE]:
        doc = self.collection.document(id).get()
        if doc.exists:
            return self._from_dict(doc.id, doc.to_dict())
        return None

    def get_by_semestre(self, semestre: Any) -> List[UE]:
        """Récupère toutes les UEs d'un semestre (supporte l'index int)."""
        # On force la recherche sur l'entier
        try:
            s_int = int(semestre)
        except (ValueError, TypeError):
            s_int = semestre
            
        docs = self.collection.where('semestre_id', '==', s_int).stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def list_all(self) -> List[UE]:
        docs = self.collection.stream()
        return [self._from_dict(doc.id, doc.to_dict()) for doc in docs]

    def delete(self, id: str) -> None:
        self.collection.document(id).delete()
