from abc import ABC, abstractmethod
from typing import Optional

class IConfigRepository(ABC):
    @abstractmethod
    def get_value(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    def set_value(self, key: str, value: str, description: str = "") -> None:
        pass
