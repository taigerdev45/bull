from typing import Dict, Any
from infrastructure.persistence.firebase.connection import FirebaseConnection

class FirebaseConfigRepository:
    """Gère la configuration globale du système dans Firestore."""

    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('system_config')
        self.doc_id = 'global_settings'

    def get_settings(self) -> Dict[str, Any]:
        """Récupère les paramètres actuels."""
        doc = self.collection.document(self.doc_id).get()
        if doc.exists:
            return doc.to_dict()
        return self._get_defaults()

    def update_settings(self, settings: Dict[str, Any]) -> None:
        """Met à jour les paramètres."""
        self.collection.document(self.doc_id).set(settings, merge=True)

    def _get_defaults(self) -> Dict[str, Any]:
        """Valeurs par défaut (issues de constants.py)."""
        return {
            'reprise_soutenance_active': True,
            'reprise_soutenance_ues_exclues': ['UE6-2'],
            'penalite_absence_par_heure': 0.01,
            'seuil_validation_mention': [10.0, 12.0, 14.0, 16.0],
            'date_verrouillage_notes': None
        }
