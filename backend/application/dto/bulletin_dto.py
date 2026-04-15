from pydantic import BaseModel, Field, validator
from typing import List, Optional

class EtudiantDTO(BaseModel):
    """DTO pour l'affichage des informations d'un étudiant."""
    id: str
    nom: str
    prenom: str
    matricule: str
    date_naissance: str

class EvaluationDTO(BaseModel):
    """DTO pour la saisie ou l'affichage d'une note."""
    id: Optional[str] = None
    etudiant_id: str
    matiere_id: str
    type_eval: str = Field(..., pattern="^(CC|EXAMEN|RATTRAPAGE)$")
    note: float = Field(..., ge=0, le=20)

    @validator('note')
    def validate_note_range(cls, v):
        if not (0 <= v <= 20):
            raise ValueError("La note doit être entre 0 et 20")
        return v

class ResultatUEDTO(BaseModel):
    """DTO pour le résultat d'une Unité d'Enseignement."""
    ue_code: str
    ue_libelle: str
    moyenne: float
    etat: str
    credits: int

from application.dto.resultat_dto import ResultatSemestreDTO, ResultatAnnuelDTO

class BulletinDTO(BaseModel):
    """DTO complet pour la génération d'un bulletin de notes."""
    etudiant: EtudiantDTO
    type_bulletin: str # SEMESTRIEL | ANNUEL
    resultat_semestre: Optional[ResultatSemestreDTO] = None
    resultat_annuel: Optional[ResultatAnnuelDTO] = None
    date_generation: str
    saisie_par: str
