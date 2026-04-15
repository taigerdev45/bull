from domain.events.evaluation_creee import EvaluationCreee
from domain.events.evaluation_modifiee import EvaluationModifiee
from domain.events.evaluation_supprimee import EvaluationSupprimee

class AuditLogHandler:
    """Consomme les événements de domaine pour alimenter les logs d'audit."""

    def __init__(self, audit_service: 'AuditService'):
        self.audit_service = audit_service

    def handle_evaluation_creee(self, event: EvaluationCreee):
        log_data = {
            'utilisateur_id': event.metadata.get('user_id'),
            'utilisateur_email': event.metadata.get('user_email'),
            'action': 'CREATION',
            'entite': 'Evaluation',
            'entite_id': event.data.get('evaluation_id'),
            'etudiant_concerne': event.data.get('etudiant_id'),
            'ip_address': event.metadata.get('ip_address'),
            'user_agent': event.metadata.get('user_agent'),
            'details': {
                'matiere': event.data.get('matiere_libelle'),
                'type_evaluation': event.data.get('type_eval'),
                'nouvelle_valeur': event.data.get('note')
            }
        }
        self.audit_service.logger_action(log_data)

    def handle_evaluation_modifiee(self, event: EvaluationModifiee):
        log_data = {
            'utilisateur_id': event.metadata.get('user_id'),
            'utilisateur_email': event.metadata.get('user_email'),
            'action': 'MODIFICATION',
            'entite': 'Evaluation',
            'entite_id': event.data.get('evaluation_id'),
            'etudiant_concerne': event.data.get('etudiant_id'),
            'ip_address': event.metadata.get('ip_address'),
            'user_agent': event.metadata.get('user_agent'),
            'details': {
                'matiere': event.data.get('matiere_libelle'),
                'type_evaluation': event.data.get('type_eval'),
                'ancienne_valeur': event.data.get('ancienne_note'),
                'nouvelle_valeur': event.data.get('nouvelle_note')
            }
        }
        self.audit_service.logger_action(log_data)

    def handle_evaluation_supprimee(self, event: EvaluationSupprimee):
        log_data = {
            'utilisateur_id': event.metadata.get('user_id'),
            'utilisateur_email': event.metadata.get('user_email'),
            'action': 'SUPPRESSION',
            'entite': 'Evaluation',
            'entite_id': event.data.get('evaluation_id'),
            'etudiant_concerne': event.data.get('etudiant_id'),
            'ip_address': event.metadata.get('ip_address'),
            'user_agent': event.metadata.get('user_agent'),
            'details': {
                'matiere': event.data.get('matiere_libelle'),
                'type_evaluation': event.data.get('type_eval'),
                'ancienne_valeur': event.data.get('derniere_note')
            }
        }
        self.audit_service.logger_action(log_data)
