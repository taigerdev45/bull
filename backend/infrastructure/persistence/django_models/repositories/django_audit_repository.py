from typing import Dict, Any, List, Optional
from domain.repositories.i_audit_repository import IAuditRepository
from infrastructure.persistence.django_models.models import AuditLogModel

class DjangoAuditRepository(IAuditRepository):
    def save(self, log_data: Dict[str, Any]) -> None:
        AuditLogModel.objects.create(
            action=log_data.get('action'),
            utilisateur_uid=log_data.get('utilisateur_uid'),
            details=log_data.get('details'),
            entity_id=log_data.get('entity_id'),
            entity_type=log_data.get('entity_type')
        )

    def search_by_etudiant(self, etudiant_id: str, action: Optional[str] = None, 
                           date_debut: Optional[str] = None, date_fin: Optional[str] = None) -> List[Dict]:
        query = AuditLogModel.objects.filter(entity_id=etudiant_id, entity_type='etudiant')
        if action:
            query = query.filter(action=action)
        if date_debut:
            query = query.filter(created_at__gte=date_debut)
        if date_fin:
            query = query.filter(created_at__lte=date_fin)
            
        models = query.order_by('-created_at')
        return [self._to_dict(m) for m in models]

    def get_all(self, filtres: Optional[Dict] = None) -> List[Dict]:
        query = AuditLogModel.objects.all()
        if filtres:
            if filtres.get('action'):
                query = query.filter(action=filtres.get('action'))
            if filtres.get('entity_type'):
                query = query.filter(entity_type=filtres.get('entity_type'))
            if filtres.get('date_debut'):
                query = query.filter(created_at__gte=filtres.get('date_debut'))
            if filtres.get('date_fin'):
                query = query.filter(created_at__lte=filtres.get('date_fin'))
        
        models = query.order_by('-created_at')[:500]  # Limite raisonnable
        return [self._to_dict(m) for m in models]

    def _to_dict(self, model: AuditLogModel) -> Dict:
        return {
            'action': model.action,
            'utilisateur_uid': model.utilisateur_uid,
            'details': model.details,
            'entity_id': model.entity_id,
            'entity_type': model.entity_type,
            'timestamp': model.created_at.isoformat()
        }
