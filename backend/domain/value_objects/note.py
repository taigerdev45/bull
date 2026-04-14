from dataclasses import dataclass
from typing import ClassVar

@dataclass(frozen=True)
class Note:
    """Objet Valeur immuable représentant une Note."""
    value: float
    MIN_VALUE: ClassVar[float] = 0.0
    MAX_VALUE: ClassVar[float] = 20.0

    def __post_init__(self):
        if not (self.MIN_VALUE <= self.value <= self.MAX_VALUE):
            raise ValueError(f"La note doit être comprise entre {self.MIN_VALUE} et {self.MAX_VALUE}")

    def __str__(self):
        return f"{self.value:.2f}/20"
