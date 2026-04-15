from typing import List, Optional
from domain.entities.resultat import ResultatUE, ResultatSemestre, ResultatAnnuel
from domain.repositories.i_resultat_repository import IResultatRepository
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebaseResultatRepository(IResultatRepository):
    """Implémentation du repository Résultats avec Firestore."""

    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.coll_ue = self.db.collection('resultats_ue')
        self.coll_semestre = self.db.collection('resultats_semestre')
        self.coll_annuel = self.db.collection('resultats_annuel')

    def save_ue(self, resultat: ResultatUE) -> None:
        data = {
            'etudiant_id': resultat._etudiant_id,
            'ue_id': resultat._ue_id,
            'moyenne': resultat._moyenne.valeur,
            'details': resultat._moyenne.details
        }
        self.coll_ue.document(resultat.id).set(data)

    def save_semestre(self, resultat: ResultatSemestre) -> None:
        # Logique similaire pour semestre...
        pass

    def save_annuel(self, resultat: ResultatAnnuel) -> None:
        # Logique similaire pour annuel...
        pass

    def get_par_etudiant_semestre(self, etudiant_id: str, semestre: int) -> Optional[ResultatSemestre]:
        docs = self.coll_semestre.where('etudiant_id', '==', etudiant_id)\
                                 .where('semestre', '==', semestre).stream()
        for doc in docs:
            # Mapping vers entité à faire
            pass
        return None

    def get_par_etudiant_annuel(self, etudiant_id: str) -> Optional[ResultatAnnuel]:
        docs = self.coll_annuel.where('etudiant_id', '==', etudiant_id).stream()
        for doc in docs:
            pass
        return None

    def obtenir_ue_details(self, etudiant_id: str, semestre: int) -> List[ResultatUE]:
        docs = self.coll_ue.where('etudiant_id', '==', etudiant_id).stream()
        # Filtrage UE par semestre nécessiterait de joindre avec Matiere/UE
        return []
