from typing import Dict, Any, List
from domain.repositories.i_audit_repository import IAuditRepository


class AuditService:
    """Service centralisant la journalisation des actions pour traçabilité."""

    def __init__(self, audit_repo: IAuditRepository):
        self.audit_repo = audit_repo

    def logger_action(self, log_data: Dict[str, Any]) -> None:
        """Enregistre un log d'audit."""
        self.audit_repo.save(log_data)

    def obtenir_audit_etudiant(self, etudiant_id: str, filtres: Dict = None) -> List[Dict]:
        """Récupère l'historique d'audit pour un étudiant."""
        filtres = filtres or {}
        return self.audit_repo.search_by_etudiant(
            etudiant_id=etudiant_id,
            action=filtres.get('action'),
            date_debut=filtres.get('date_debut'),
            date_fin=filtres.get('date_fin')
        )

    def obtenir_tous_les_logs(self, filtres: Dict = None) -> List[Dict]:
        """Récupère tous les logs avec filtres optionnels."""
        return self.audit_repo.get_all(filtres)
