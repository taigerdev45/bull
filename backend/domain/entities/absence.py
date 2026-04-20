from datetime import date
from .base_entity import BaseEntity
from domain.exceptions.domain_exception import ValidationException

class Absence(BaseEntity):
    """
    Entité représentant une absence d'un étudiant dans une matière.
    """

    def __init__(self, etudiant_id: str, matiere_id: str, nombre_heures: int, 
                 date_absence: date, saisie_par: str, id: str = None):
        super().__init__(id)
        self._etudiant_id = etudiant_id
        self._matiere_id = matiere_id
        self._nombre_heures = nombre_heures
        self._date_absence = date_absence
        self._saisie_par = saisie_par
        self.valider()

    @property
    def etudiant_id(self) -> str:
        return self._etudiant_id

    @property
    def matiere_id(self) -> str:
        return self._matiere_id

    @property
    def nombre_heures(self) -> int:
        return self._nombre_heures

    @property
    def date_absence(self) -> date:
        return self._date_absence

    @property
    def saisie_par(self) -> str:
        return self._saisie_par

    def valider(self):
        """Vérifie la validité des données d'absence."""
        if self._nombre_heures < 0:
            raise ValidationException("Le nombre d'heures d'absence ne peut pas être négatif.")
        
        if self._date_absence > date.today():
            raise ValidationException("La date d'absence ne peut pas être dans le futur.")

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'etudiant_id': self._etudiant_id,
            'matiere_id': self._matiere_id,
            'nombre_heures': self._nombre_heures,
            'date_absence': self._date_absence.isoformat(),
            'saisie_par': self._saisie_par,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
