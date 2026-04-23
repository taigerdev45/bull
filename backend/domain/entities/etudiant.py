from typing import List, Optional
from datetime import date
from domain.entities.base_entity import BaseEntity
from domain.exceptions.domain_exception import ValidationException

class Etudiant(BaseEntity):
    """Entité Étudiant avec gestion de ses évaluations."""

    def __init__(self, nom: str, prenom: str, matricule: str, date_naissance: date, 
                 email: str, user_id: Optional[str] = None,
                 lieu_naissance: Optional[str] = None, bac: Optional[str] = None, 
                 provenance: Optional[str] = None, id: Optional[str] = None):
        super().__init__(id)
        self._nom = nom
        self._prenom = prenom
        self._matricule = matricule
        self._email = email
        self._user_id = user_id
        self._date_naissance = date_naissance
        self._lieu_naissance = lieu_naissance
        self._bac = bac
        self._provenance = provenance
        self._evaluations_ids: List[str] = []

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def prenom(self) -> str:
        return self._prenom

    @property
    def email(self) -> str:
        return self._email

    @property
    def user_id(self) -> Optional[str]:
        return self._user_id

    @property
    def nom_complet(self) -> str:
        return f"{self._prenom} {self._nom}"

    @property
    def matricule(self) -> str:
        return self._matricule

    @property
    def date_naissance(self):
        return self._date_naissance

    @property
    def lieu_naissance(self) -> Optional[str]:
        return self._lieu_naissance

    @property
    def bac(self) -> Optional[str]:
        return self._bac

    @property
    def provenance(self) -> Optional[str]:
        return self._provenance

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
        if not self._email or "@" not in self._email:
            raise ValidationException("Un email valide est obligatoire.")

    def __repr__(self):
        return f"<Etudiant {self._matricule}: {self.nom_complet}>"
