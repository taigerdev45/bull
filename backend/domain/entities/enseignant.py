from typing import Optional, List
from domain.entities.base_entity import BaseEntity
from domain.exceptions.domain_exception import ValidationException

class Enseignant(BaseEntity):
    """
    Entité représentant un enseignant.
    """

    def __init__(self, nom: str, prenom: str, email: str, matricule: str, 
                 user_id: Optional[str] = None, id: Optional[str] = None):
        super().__init__(id)
        self._nom = nom
        self._prenom = prenom
        self._email = email
        self._matricule = matricule
        self._user_id = user_id
        self._matiere_ids: List[str] = []

    @property
    def matricule(self) -> str:
        return self._matricule

    @property
    def user_id(self) -> Optional[str]:
        return self._user_id

    @property
    def nom_complet(self) -> str:
        return f"{self._prenom} {self._nom}"

    @property
    def email(self) -> str:
        return self._email

    def assigner_matiere(self, matiere_id: str):
        if matiere_id not in self._matiere_ids:
            self._matiere_ids.append(matiere_id)
            self.update_timestamp()

    def valider(self):
        if not self._nom or not self._prenom:
            raise ValidationException("Le nom et le prénom de l'enseignant sont obligatoires.")
        if not self._matricule or not self._matricule.startswith("ENS-"):
            raise ValidationException("Le matricule enseignant doit commencer par 'ENS-'.")
        if "@" not in self._email:
            raise ValidationException("Email invalide.")

    def __repr__(self):
        return f"<Enseignant {self.nom_complet}>"
