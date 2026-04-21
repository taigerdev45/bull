from typing import Optional
from domain.entities.base_entity import BaseEntity
from domain.exceptions.domain_exception import ValidationException

class Personnel(BaseEntity):
    """
    Entité représentant le personnel administratif (Admin, Secrétariat).
    """

    def __init__(self, nom: str, prenom: str, email: str, role: str, 
                 numero_telephone: Optional[str] = None,
                 derniere_connexion: Optional[str] = None,
                 user_id: Optional[str] = None, id: Optional[str] = None):
        super().__init__(id)
        self._nom = nom
        self._prenom = prenom
        self._email = email
        self._numero_telephone = numero_telephone
        self._derniere_connexion = derniere_connexion
        self._role = role # 'admin' or 'secretariat' or 'super_admin' or 'enseignant'
        self._user_id = user_id

    @property
    def nom_complet(self) -> str:
        return f"{self._prenom} {self._nom}"

    @property
    def email(self) -> str:
        return self._email

    @property
    def role(self) -> str:
        return self._role

    @property
    def numero_telephone(self) -> Optional[str]:
        return self._numero_telephone

    @property
    def derniere_connexion(self) -> Optional[str]:
        return self._derniere_connexion

    @property
    def user_id(self) -> Optional[str]:
        return self._user_id

    def enregistrer_connexion(self):
        from datetime import datetime
        self._derniere_connexion = datetime.now().isoformat()
        self.update_timestamp()

    def valider(self):
        if not self._nom or not self._prenom:
            raise ValidationException("Le nom et le prénom sont obligatoires.")
        if "@" not in self._email:
            raise ValidationException("Email invalide.")
        if self._role not in ['admin', 'secretariat', 'super_admin', 'enseignant']:
            raise ValidationException("Rôle invalide.")

    def __repr__(self):
        return f"<Personnel {self._role}: {self.nom_complet}>"
