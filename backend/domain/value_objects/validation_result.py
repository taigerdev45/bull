from dataclasses import dataclass
from enum import Enum, auto

class EtatAcquisition(Enum):
    ACQUISE_DIRECTE = auto()
    COMPENSEE = auto()
    NON_ACQUISE = auto()

@dataclass(frozen=True)
class ValidationResult:
    """Objet Valeur représentant le résultat d'une validation d'UE ou de Semestre."""
    etat: EtatAcquisition
    credits_acquis: int
    moyenne: float
    message: str = ""
