from typing import List, Dict, Any, Optional
from datetime import datetime
from ..django_models.models import AuditLogModel

class SQLiteAuditRepository:
    """Implémentation du repository Audit utilisant l'ORM Django (SQLite/Turso)."""

    def save(self, log_data: Dict[str, Any]) -> None:
        AuditLogModel.objects.create(
            action=log_data.get('action', 'Unknown'),
            utilisateur_uid=log_data.get('utilisateur_uid', 'System'),
            details=str(log_data.get('details', '')),
            entity_id=log_data.get('entity_id'),
            entity_type=log_data.get('entity_type')
        )

    def search_by_etudiant(self, etudiant_id: str, date_debut: datetime = None, date_fin: datetime = None, action: str = None) -> List[Dict[str, Any]]:
        query = AuditLogModel.objects.filter(entity_id=etudiant_id, entity_type='Etudiant')
        if action:
            query = query.filter(action=action)
        if date_debut:
            query = query.filter(created_at__gte=date_debut)
        if date_fin:
            query = query.filter(created_at__lte=date_fin)
            
        models = query.order_by('-created_at')
        return [
            {
                'id': m.id,
                'action': m.action,
                'utilisateur_uid': m.utilisateur_uid,
                'details': m.details,
                'entity_id': m.entity_id,
                'entity_type': m.entity_type,
                'timestamp': m.created_at
            } for m in models
        ]
