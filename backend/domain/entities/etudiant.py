from typing import List, Optional
from datetime import date
from domain.entities.base_entity import BaseEntity
from domain.exceptions.domain_exception import ValidationException

class Etudiant(BaseEntity):
    """Entité Étudiant avec gestion de ses évaluations."""

    def __init__(self, nom: str, prenom: str, matricule: str, date_naissance: date, id: Optional[str] = None):
        super().__init__(id)
        self._nom = nom
        self._prenom = prenom
        self._matricule = matricule
        self._date_naissance = date_naissance
        self._evaluations_ids: List[str] = []

    @property
    def nom_complet(self) -> str:
        return f"{self._prenom} {self._nom}"

    @property
    def matricule(self) -> str:
        return self._matricule

    def ajouter_evaluation(self, evaluation_id: str):
        """Associe une évaluation à l'étudiant."""
        if evaluation_id not in self._evaluations_ids:
            self._evaluations_ids.append(evaluation_id)
            self.update_timestamp()

    def valider(self):
        """Vérifie l'intégrité de l'étudiant."""
        if not self._nom or not self._prenom:
            raise ValidationException("Le nom et le prénom sont obligatoires.")
        if not self._matricule:
            raise ValidationException("Le matricule est obligatoire.")

    def __repr__(self):
        return f"<Etudiant {self._matricule}: {self.nom_complet}>"
