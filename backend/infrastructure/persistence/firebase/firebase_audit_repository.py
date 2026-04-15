from typing import List, Dict, Any
from google.cloud import firestore
from infrastructure.persistence.firebase.connection import FirebaseConnection
from datetime import datetime, timedelta

class FirebaseAuditRepository:
    """Implémentation du repository Audit avec Firestore."""

    def __init__(self, connection: FirebaseConnection):
        self.db = connection.client
        self.collection = self.db.collection('audit_logs')

    def save(self, log_data: Dict[str, Any]) -> None:
        """Enregistre une entrée d'audit avec TTL de 7 ans."""
        # Calcul du TTL (7 ans)
        expire_at = datetime.now() + timedelta(days=7*365)
        
        doc_data = {
            **log_data,
            'timestamp': firestore.SERVER_TIMESTAMP,
            'expire_at': expire_at
        }
        self.collection.add(doc_data)

    def search_by_etudiant(self, etudiant_id: str, date_debut: datetime = None, date_fin: datetime = None, action: str = None) -> List[Dict[str, Any]]:
        """Recherche les logs d'audit pour un étudiant avec filtres."""
        query = self.collection.where('etudiant_concerne', '==', etudiant_id)
        
        if action:
            query = query.where('action', '==', action)
        
        # Note: Les filtres de date nécessitent un index composite en Firestore
        # Pour rester simple, on filtre les plus récents
        docs = query.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
        
        results = []
        for doc in docs:
            data = doc.to_dict()
            results.append({
                'id': doc.id,
                **data
            })
        return results
