from domain.entities.base_entity import BaseEntity
from typing import Optional

class Etudiant(BaseEntity):
    """Entité Étudiant avec encapsulation stricte."""

    def __init__(self, nom: str, prenom: str, matricule: str, id: Optional[str] = None):
        super().__init__(id)
        self._nom = nom
        self._prenom = prenom
        self._matricule = matricule

    @property
    def nom(self) -> str:
        return self._nom

    @nom.setter
    def nom(self, value: str):
        if not value:
            raise ValueError("Le nom ne peut pas être vide")
        self._nom = value
        self.update_timestamp()

    @property
    def prenom(self) -> str:
        return self._prenom

    @property
    def matricule(self) -> str:
        return self._matricule

    @property
    def nom_complet(self) -> str:
        return f"{self._prenom} {self._nom}"

    def __repr__(self):
        return f"<Etudiant {self._matricule}: {self.nom_complet}>"
