from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass(frozen=True)
class EtudiantDTO:
    id: str
    nom: str
    prenom: str
    matricule: str
    date_naissance: str

@dataclass(frozen=True)
class EvaluationDTO:
    id: str
    etudiant_id: str
    matiere_id: str
    type: str # CC, EXAMEN, RATTRAPAGE
    note: Optional[float]

@dataclass(frozen=True)
class ResultatUEDTO:
    ue_code: str
    ue_libelle: str
    moyenne: float
    etat: str # ACQUISE, COMPENSEE, ECHEC
    credits: int

@dataclass(frozen=True)
class BulletinDTO:
    etudiant: EtudiantDTO
    semestre: int
    moyenne_generale: float
    total_credits: int
    resultats_ues: List[ResultatUEDTO]
    mention: str
    decision_jury: str
