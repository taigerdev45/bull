from enum import Enum, auto
from typing import Optional
from domain.entities.base_entity import BaseEntity
from domain.value_objects.note import Note
from domain.exceptions.domain_exception import ValidationException

class TypeEvaluation(Enum):
    CC = auto()
    EXAMEN = auto()
    RATTRAPAGE = auto()

class Evaluation(BaseEntity):
    """Entité représentant une évaluation d'un étudiant pour une matière."""

    def __init__(self, etudiant_id: str, matiere_id: str, type: TypeEvaluation, note: Note, id: Optional[str] = None):
        super().__init__(id)
        self._etudiant_id = etudiant_id
        self._matiere_id = matiere_id
        self._type = type
        self._note = note

    @property
    def note_valeur(self) -> Optional[float]:
        return self._note.valeur

    @property
    def type(self) -> TypeEvaluation:
        return self._type

    def valider(self):
        if not self._etudiant_id or not self._matiere_id:
            raise ValidationException("L'ID étudiant et l'ID matière sont obligatoires.")

    def __repr__(self):
        return f"<Evaluation {self._type.name} - Note: {self._note}>"
