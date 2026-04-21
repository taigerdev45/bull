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

    def __init__(self, etudiant_id: str, matiere_id: str, type: TypeEvaluation, note: Note, 
                 date_saisie: Optional[str] = None, saisie_par: Optional[str] = None, 
                 enseignant_id: Optional[str] = None, id: Optional[str] = None):
        super().__init__(id)
        self._etudiant_id = etudiant_id
        self._matiere_id = matiere_id
        self._enseignant_id = enseignant_id
        self._type = type
        self._note = note
        self._date_saisie = date_saisie
        self._saisie_par = saisie_par
        self._deleted_at = None
        self._verrouille = False
        self._historique = []

    @property
    def etudiant_id(self) -> str:
        return self._etudiant_id

    @property
    def matiere_id(self) -> str:
        return self._matiere_id

    @property
    def enseignant_id(self) -> Optional[str]:
        return self._enseignant_id

    @property
    def date_saisie(self) -> Optional[str]:
        return self._date_saisie

    @property
    def saisie_par(self) -> Optional[str]:
        return self._saisie_par

    @property
    def note_valeur(self) -> Optional[float]:
        return self._note.valeur

    @property
    def note(self) -> Note:
        return self._note

    @property
    def type(self) -> TypeEvaluation:
        return self._type

    @property
    def est_supprime(self) -> bool:
        return self._deleted_at is not None

    @property
    def est_verrouille(self) -> bool:
        return self._verrouille

    def marquer_supprime(self):
        from datetime import datetime
        self._deleted_at = datetime.now().isoformat()
        self.update_timestamp()

    def verrouiller(self):
        self._verrouille = True
        self.update_timestamp()

    def modifier_note(self, nouvelle_note: Note, auteur: str):
        if self._verrouille:
            raise ValidationException("Impossible de modifier une note verrouillée par le jury.")
        
        # Historique
        self._historique.append({
            'ancienne_valeur': self._note.valeur,
            'date_modif': self._date_saisie,
            'auteur': self._saisie_par
        })
        
        self._note = nouvelle_note
        self._saisie_par = auteur
        from datetime import datetime
        self._date_saisie = datetime.now().isoformat()
        self.update_timestamp()

    def valider(self):
        if not self._etudiant_id or not self._matiere_id:
            raise ValidationException("L'ID étudiant et l'ID matière sont obligatoires.")

    def __repr__(self):
        return f"<Evaluation {self._type.name} - Note: {self._note}>"
