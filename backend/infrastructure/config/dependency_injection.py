from typing import Dict, Any, Type, TypeVar
import threading

T = TypeVar("T")

class DIContainer:
    """Conteneur d'injection de dépendances (Simple Container Pattern)."""
    _instance = None
    _lock = threading.Lock()
    _services: Dict[Type, Any] = {}

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DIContainer, cls).__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, interface: Type[T], implementation: Any):
        """Enregistre une implémentation pour une interface donnée."""
        cls._services[interface] = implementation

    @classmethod
    def resolve(cls, interface: Type[T]) -> T:
        """Résout et retourne l'instance d'une interface."""
        implementation = cls._services.get(interface)
        if not implementation:
            raise Exception(f"Service non enregistré pour l'interface : {interface.__name__}")
        
        # Si c'est une classe, on l'instancie (Simple Singleton behavior for dependencies)
        if isinstance(implementation, type):
            cls._services[interface] = implementation()
            return cls._services[interface]
            
        return implementation

# Instance globale pour un accès facile (Facultatif, dépend du design souhaité)
container = DIContainer()
