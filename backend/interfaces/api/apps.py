from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'interfaces.api'
    verbose_name = 'Bulletin API'

    def ready(self):
        """
        Initialisation de l'application et wiring de l'injection de dépendances.
        Cette méthode est appelée une seule fois au démarrage de Django.
        """
        from infrastructure.config.dependency_injection import Container
        
        # Initialisation du conteneur
        container = Container()
        
        # Wiring : Branchement du conteneur sur les packages qui utilisent @inject
        # On définit les modules cibles pour que les décorateurs @inject soient résolus.
        container.wire(packages=[
            "interfaces.api.views",
            "application.services",
            "application.commands",
            "application.handlers",
            "domain.services",
            "domain.events.handlers"
        ])
        
        logger.info("Injection de dépendances (Dependency Injector) : Wiring terminé pour Bulletin API.")
