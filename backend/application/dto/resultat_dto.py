from pydantic import BaseModel
from typing import List, Optional, Dict

class MatiereDetailDTO(BaseModel):
    """Détail des notes pour une matière."""
    id: str
    libelle: str
    coefficient: float
    note_cc: Optional[float] = None
    note_examen: Optional[float] = None
    note_rattrapage: Optional[float] = None
    moyenne: float
    penalite: float = 0.0

class UEDetailDTO(BaseModel):
    """Détail des résultats pour une Unité d'Enseignement."""
    id: str
    code: str
    libelle: str
    moyenne_ue: float
    statut: str  # ACQUISE, COMPENSEE, NON_ACQUISE
    credits_acquis: int
    compensee: bool
    matieres: List[MatiereDetailDTO]

class ResultatSemestreDTO(BaseModel):
    """Résultat global pour un semestre."""
    etudiant_id: str
    semestre: int
    moyenne_generale: float
    credits_acquis: int
    total_credits: int
    valide: bool
    ues: List[UEDetailDTO]

class ResultatAnnuelDTO(BaseModel):
    """Résultat global pour une année universitaire (S5+S6)."""
    etudiant_id: str
    moyenne_annuelle: float
    total_credits: int
    decision: str  # ADMIS, ADMIS_COMPENSE, AJOURNE
    mention: str
    semestres: Dict[str, ResultatSemestreDTO]
