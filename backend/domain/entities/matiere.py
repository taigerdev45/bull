from typing import Optional
from domain.entities.base_entity import BaseEntity
from domain.value_objects.coefficient import Coefficient
from domain.exceptions.domain_exception import ValidationException

class Matiere(BaseEntity):
    """Entité représentant une matière d'enseignement."""

    def __init__(self, libelle: str, coefficient: Coefficient, credits: int, ue_id: str, 
                 enseignant_id: Optional[str] = None, id: Optional[str] = None):
        super().__init__(id)
        self._libelle = libelle
        self._coefficient = coefficient
        self._credits = credits
        self._ue_id = ue_id
        self._enseignant_id = enseignant_id

    @property
    def libelle(self) -> str:
        return self._libelle

    @property
    def coefficient(self) -> float:
        return self._coefficient.valeur

    @property
    def credits(self) -> int:
        return self._credits

    def valider(self):
        if not self._libelle:
            raise ValidationException("Le libellé de la matière est obligatoire.")
        if not self._ue_id:
            raise ValidationException("L'ID de l'UE est obligatoire pour une matière.")
        if self._credits < 0:
            raise ValidationException("Les crédits ne peuvent pas être négatifs.")

    def __repr__(self):
        return f"<Matiere {self._libelle} (Coeff: {self.coefficient})>"
