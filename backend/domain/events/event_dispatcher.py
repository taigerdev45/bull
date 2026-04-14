from typing import Dict, List, Callable, Type
from domain.events.event import Event

class EventDispatcher:
    """Dispatcheur d'événements implémentant le pattern Observer."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventDispatcher, cls).__new__(cls)
            cls._instance._listeners: Dict[Type[Event], List[Callable]] = {}
        return cls._instance

    def subscribe(self, event_type: Type[Event], handler: Callable):
        """Abonne un gestionnaire à un type d'événement."""
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(handler)

    def dispatch(self, event: Event):
        """Diffuse un événement à tous ses abonnés."""
        event_type = type(event)
        if event_type in self._listeners:
            for handler in self._listeners[event_type]:
                handler(event)

# Instance globale (Singleton)
dispatcher = EventDispatcher()
