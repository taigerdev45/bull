from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ListerEvaluationsEtudiantQuery:
    """Requête de lecture pour l'historique des notes."""
    etudiant_id: str
    semestre: Optional[int] = None
    ue_id: Optional[str] = None
    matiere_id: Optional[str] = None
