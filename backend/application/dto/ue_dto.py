from pydantic import BaseModel
from typing import List, Optional

class MatiereDTO(BaseModel):
    """Représente une matière pédagogique."""
    id: str
    libelle: str
    coefficient: float
    credits: int
    ue_id: str
    enseignant_id: Optional[str] = None

class UEDTO(BaseModel):
    """Représente une Unité d'Enseignement (UE)."""
    id: str
    code: str
    libelle: str
    credits: int
    semestre: int
    matieres: List[MatiereDTO] = []
