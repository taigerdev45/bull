from typing import Dict, List, Optional
from domain.entities.base_entity import BaseEntity
from domain.entities.resultat import ResultatSemestre
from domain.value_objects.moyenne import Moyenne
from domain.exceptions.domain_exception import ValidationException

class Bulletin(BaseEntity):
    """
    Entité Aggregate Root représentant le bulletin de notes d'un étudiant.
    Regroupe les résultats par semestre et les informations globales.
    """

    def __init__(self, 
                 etudiant_id: str, 
                 nom_etudiant: str,
                 prenom_etudiant: str,
                 matricule: str,
                 annee_academique: str,
                 id: Optional[str] = None):
        super().__init__(id)
        self._etudiant_id = etudiant_id
        self._nom_etudiant = nom_etudiant
        self._prenom_etudiant = prenom_etudiant
        self._matricule = matricule
        self._annee_academique = annee_academique
        self._semestres: Dict[int, ResultatSemestre] = {}
        self._moyenne_annuelle: Optional[Moyenne] = None
        self._mention: Optional[str] = None

    @property
    def etudiant_id(self) -> str:
        return self._etudiant_id

    @property
    def matricule(self) -> str:
        return self._matricule

    @property
    def moyenne_annuelle(self) -> Optional[Moyenne]:
        return self._moyenne_annuelle

    def ajouter_semestre(self, semestre_index: int, resultat: ResultatSemestre):
        """Ajoute ou met à jour les résultats d'un semestre."""
        if not (1 <= semestre_index <= 8):
            raise ValidationException("Index de semestre invalide.")
        self._semestres[semestre_index] = resultat
        self.update_timestamp()

    def set_resultat_annuel(self, moyenne: Moyenne):
        """Définit la moyenne annuelle et la déduction de la mention."""
        self._moyenne_annuelle = moyenne
        if moyenne.details and 'mention' in moyenne.details:
            self._mention = moyenne.details['mention']
        self.update_timestamp()

    def valider(self):
        if not self._etudiant_id or not self._matricule:
            raise ValidationException("ID étudiant et matricule requis pour le bulletin.")

    def __repr__(self):
        return f"<Bulletin {self._matricule} - {self._annee_academique}>"
