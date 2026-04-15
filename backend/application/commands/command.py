from abc import ABC, abstractmethod

class Command(ABC):
    """Interface de base pour toutes les commandes."""
    @abstractmethod
    def executer(self) -> any:
        pass