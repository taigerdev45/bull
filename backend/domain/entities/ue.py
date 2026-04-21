from typing import List, Optional, Dict
from domain.entities.base_entity import BaseEntity
from domain.exceptions.domain_exception import ValidationException
from domain.value_objects.moyenne import Moyenne, TypeCalculMoyenne

class UE(BaseEntity):
    """Entité Unité d'Enseignement (UE)."""

    def __init__(self, code: str, libelle: str, credits: int, semestre_id: str, id: Optional[str] = None):
        super().__init__(id)
        self._code = code
        self._libelle = libelle
        self._credits = credits
        self._semestre_id = semestre_id
        self._matieres_ids: List[str] = []

    @property
    def code(self) -> str:
        return self._code

    @property
    def libelle(self) -> str:
        return self._libelle

    @property
    def credits(self) -> int:
        return self._credits

    def ajouter_matiere(self, matiere_id: str):
        if matiere_id not in self._matieres_ids:
            self._matieres_ids.append(matiere_id)
            self.update_timestamp()

    def calculer_moyenne_ponderee(self, notes_par_matiere: Dict[str, float], coeffs_par_matiere: Dict[str, float]) -> Moyenne:
        """Calcule la moyenne de l'UE sur la base des coefficients des matières."""
        total_poids = 0.0
        somme_ponderee = 0.0
        
        for m_id in self._matieres_ids:
            if m_id in notes_par_matiere and m_id in coeffs_par_matiere:
                note = notes_par_matiere[m_id]
                coeff = coeffs_par_matiere[m_id]
                somme_ponderee += note * coeff
                total_poids += coeff
        
        if total_poids == 0:
            return Moyenne(0.0, TypeCalculMoyenne.PONDEREE, {"error": "Aucune note ou coefficient trouvé"})
            
        valeur_moyenne = somme_ponderee / total_poids
        return Moyenne(valeur_moyenne, TypeCalculMoyenne.PONDEREE)

    def valider(self):
        if not self._code or not self._libelle:
            raise ValidationException("Le code et le libellé de l'UE sont obligatoires.")
        if not self._semestre_id:
            raise ValidationException("Le semestre est obligatoire.")

    def __repr__(self):
        return f"<UE {self._code}: {self._libelle}>"
