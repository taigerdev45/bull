from typing import List, Optional
from datetime import date
from domain.entities.absence import Absence
from domain.repositories.i_absence_repository import IAbsenceRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebaseAbsenceRepository(IAbsenceRepository):
    """
    Implémentation Firestore du repository des absences.
    """

    def __init__(self, connection: FirebaseConnection):
        self._db = connection.client
        self._collection = self._db.collection('absences')

    def _to_firestore(self, absence: Absence) -> dict:
        return {
            'etudiant_id': absence.etudiant_id,
            'matiere_id': absence.matiere_id,
            'nombre_heures': absence.nombre_heures,
            'date_absence': absence.date_absence.isoformat(),
            'saisie_par': absence.saisie_par,
            'created_at': absence.created_at.isoformat(),
            'total_heures': absence.nombre_heures  # Utilisé pour l'indexation si besoin
        }

    def _from_firestore(self, doc_id: str, data: dict) -> Absence:
        return Absence(
            id=doc_id,
            etudiant_id=data['etudiant_id'],
            matiere_id=data['matiere_id'],
            nombre_heures=data['nombre_heures'],
            date_absence=date.fromisoformat(data['date_absence']),
            saisie_par=data['saisie_par']
        )

    def creer(self, absence: Absence) -> str:
        doc_ref = self._collection.document(absence.id)
        doc_ref.set(self._to_firestore(absence))
        return absence.id

    def modifier(self, absence: Absence) -> None:
        doc_ref = self._collection.document(absence.id)
        doc_ref.update(self._to_firestore(absence))

    def supprimer(self, absence_id: str) -> None:
        self._collection.document(absence_id).delete()

    def obtenir_par_id(self, absence_id: str) -> Optional[Absence]:
        doc = self._collection.document(absence_id).get()
        if doc.exists:
            return self._from_firestore(doc.id, doc.to_dict())
        return None

    def obtenir_par_etudiant(self, etudiant_id: str) -> List[Absence]:
        docs = self._collection.where('etudiant_id', '==', etudiant_id).stream()
        return [self._from_firestore(doc.id, doc.to_dict()) for doc in docs]

    def obtenir_par_etudiant_matiere(self, etudiant_id: str, matiere_id: str) -> List[Absence]:
        docs = self._collection.where('etudiant_id', '==', etudiant_id)\
                             .where('matiere_id', '==', matiere_id).stream()
        return [self._from_firestore(doc.id, doc.to_dict()) for doc in docs]

    def calculer_total_heures(self, etudiant_id: str, matiere_id: str) -> int:
        """
        Calcule le total des heures en agrégeant les documents Firestore.
        Note: Pour de grandes quantités, une fonction d'agrégation côté serveur serait préférable.
        """
        docs = self._collection.where('etudiant_id', '==', etudiant_id)\
                             .where('matiere_id', '==', matiere_id).stream()
        
        total = sum(doc.to_dict().get('nombre_heures', 0) for doc in docs)
        return int(total)
