from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class AbsenceDTO:
    id: str
    etudiant_id: str
    matiere_id: str
    nombre_heures: int
    date_absence: date
    saisie_par: str

@dataclass(frozen=True)
class AbsenceCreateDTO:
    etudiant_id: str
    matiere_id: str
    nombre_heures: int
    date_absence: date

@dataclass(frozen=True)
class AbsenceUpdateDTO:
    nombre_heures: Optional[int] = None
    date_absence: Optional[date] = None
