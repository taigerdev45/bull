from typing import List, Optional
from domain.entities.base_entity import BaseEntity
from domain.value_objects.moyenne import Moyenne
from domain.exceptions.domain_exception import ValidationException

class ResultatUE(BaseEntity):
    """Stockage d'un résultat calculé pour une UE."""
    def __init__(self, etudiant_id: str, ue_id: str, moyenne: Moyenne, id: Optional[str] = None):
        super().__init__(id)
        self._etudiant_id = etudiant_id
        self._ue_id = ue_id
        self._moyenne = moyenne

    def valider(self):
        if not self._etudiant_id or not self._ue_id:
            raise ValidationException("IDs manquants pour le résultat UE.")

class ResultatSemestre(BaseEntity):
    """Stockage d'un résultat calculé pour un semestre."""
    def __init__(self, etudiant_id: str, semestre: int, moyenne: Moyenne, id: Optional[str] = None):
        super().__init__(id)
        self._etudiant_id = etudiant_id
        self._semestre = semestre
        self._moyenne = moyenne

    def valider(self):
        if not (1 <= self._semestre <= 8):
            raise ValidationException("Semestre invalide.")

class ResultatAnnuel(BaseEntity):
    """Stockage d'un résultat calculé pour une année académique."""
    def __init__(self, etudiant_id: str, annee_academique: str, moyenne: Moyenne, id: Optional[str] = None):
        super().__init__(id)
        self._etudiant_id = etudiant_id
        self._annee_academique = annee_academique
        self._moyenne = moyenne

    def valider(self):
        if not self._annee_academique:
            raise ValidationException("Année académique non spécifiée.")
