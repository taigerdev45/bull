from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)  # Immutable
class Note:
    """Value Object Note avec validation métier"""
    valeur: Optional[float] = field(default=None)
    
    def __post_init__(self):
        if self.valeur is not None:
            # object.__setattr__ est nécessaire car la classe est frozen
            self._valider()
    
    def _valider(self) -> None:
        if self.valeur is not None and (self.valeur < 0 or self.valeur > 20):
            from ..exceptions.note_invalide_exception import NoteInvalideException
            raise NoteInvalideException(f"Note {self.valeur} hors limites [0, 20]")
    
    def est_presente(self) -> bool:
        return self.valeur is not None
    
    def appliquer_penalite(self, penalite: float) -> 'Note':
        """Retourne nouvelle Note avec pénalité (immuabilité)"""
        if not self.est_presente():
            return self
        nouvelle_valeur = max(0.0, self.valeur - penalite)
        return Note(round(nouvelle_valeur, 2))
    
    def __float__(self) -> float:
        return float(self.valeur) if self.valeur is not None else 0.0
    
    def __str__(self) -> str:
        return f"{self.valeur:.2f}" if self.valeur is not None else "N/A"
