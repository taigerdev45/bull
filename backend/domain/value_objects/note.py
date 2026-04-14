from dataclasses import dataclass
from typing import Optional
from domain.exceptions.domain_exception import NoteInvalideException

@dataclass(frozen=True)
class Note:
    """Objet Valeur immuable représentant une Note."""
    valeur: Optional[float] = None

    def __post_init__(self):
        if self.valeur is not None:
            if not (0 <= self.valeur <= 20):
                raise NoteInvalideException(f"La note {self.valeur} est invalide (doit être entre 0 et 20).")

    def est_presente(self) -> bool:
        """Indique si l'étudiant était présent (note non nulle)."""
        return self.valeur is not None

    def appliquer_penalite(self, points: float) -> 'Note':
        """Retourne une nouvelle Note après application d'une pénalité."""
        if not self.est_presente():
            return self
        nouvelle_valeur = max(0, self.valeur - points)
        return Note(nouvelle_valeur)

    def __str__(self):
        return f"{self.valeur:.2f}/20" if self.est_presente() else "ABS"
