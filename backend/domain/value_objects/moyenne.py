from dataclasses import dataclass
from typing import Optional
from enum import Enum, auto

class TypeCalculMoyenne(Enum):
    NORMAL = auto()           # CC + Examen
    RATTRAPAGE = auto()       # Rattrapage remplace
    UNIQUE = auto()           # Une seule note

@dataclass(frozen=True)
class Moyenne:
    """Value Object Moyenne avec contexte de calcul"""
    valeur: float
    type_calcul: TypeCalculMoyenne
    details: dict  # Traçabilité calcul
    
    def __post_init__(self):
        # Conversion forcée en float en cas de passage d'un autre type
        object.__setattr__(self, 'valeur', float(self.valeur))
        if self.valeur < 0 or self.valeur > 20:
            raise ValueError(f"Moyenne {self.valeur} invalide")
    
    def est_reussite(self, seuil: float = 10.0) -> bool:
        return self.valeur >= seuil
    
    def __float__(self) -> float:
        return self.valeur

    def __str__(self) -> str:
        return f"{self.valeur:.2f}"
