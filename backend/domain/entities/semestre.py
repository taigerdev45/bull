from typing import Optional
from domain.entities.base_entity import BaseEntity
from domain.exceptions.domain_exception import ValidationException

class Semestre(BaseEntity):
    """
    Entité représentant un semestre académique.
    Ex: Semestre 5, 2023-2024.
    """

    def __init__(self, libelle: str, annee_universitaire: str, id: Optional[str] = None):
        super().__init__(id)
        self._libelle = libelle
        self._annee_universitaire = annee_universitaire

    @property
    def libelle(self) -> str:
        return self._libelle

    @property
    def annee_universitaire(self) -> str:
        return self._annee_universitaire

    def valider(self):
        if not self._libelle or not self._annee_universitaire:
            raise ValidationException("Le libellé et l'année universitaire sont obligatoires.")

    def __repr__(self):
        return f"<Semestre {self._libelle} ({self._annee_universitaire})>"
