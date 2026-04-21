from domain.events.event_dispatcher import dispatcher
from domain.events.evaluation_creee import EvaluationCreee
from domain.events.evaluation_modifiee import EvaluationModifiee
from domain.events.evaluation_supprimee import EvaluationSupprimee
from infrastructure.config.dependency_injection import Container

def initialiser_abonnements():
    """Configure les abonnements aux événements de domaine au démarrage."""
    container = Container()
    handler = container.audit_log_handler()

    dispatcher.subscribe(EvaluationCreee, handler.handle_evaluation_creee)
    dispatcher.subscribe(EvaluationModifiee, handler.handle_evaluation_modifiee)
    dispatcher.subscribe(EvaluationSupprimee, handler.handle_evaluation_supprimee)
    
    print("[OK] Abonnements aux événements d'audit configurés.")
