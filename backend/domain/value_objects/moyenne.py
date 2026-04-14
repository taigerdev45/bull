from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict

class TypeCalculMoyenne(Enum):
    ARITHMETIQUE = auto()
    PONDEREE = auto()

@dataclass(frozen=True)
class Moyenne:
    """Objet Valeur immuable représentant une Moyenne calculée."""
    valeur: float
    type_calcul: TypeCalculMoyenne
    details: Dict = field(default_factory=dict)

    def est_reussite(self, seuil: float = 10.0) -> bool:
        """Détermine si la moyenne constitue une réussite."""
        return self.valeur >= seuil

    def __str__(self):
        return f"{self.valeur:.2f}"
