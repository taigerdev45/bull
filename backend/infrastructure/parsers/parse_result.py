from pydantic import BaseModel, Field
from typing import List, Optional
from application.dto.validation_erreur_dto import ValidationErreurDTO

class EvaluationImportDTO(BaseModel):
    """Représente une ligne d'évaluation importée depuis Excel."""
    matricule: str
    nom: str
    prenom: str
    matiere_libelle: str
    note_cc: Optional[float] = Field(None, ge=0, le=20)
    note_examen: Optional[float] = Field(None, ge=0, le=20)
    note_rattrapage: Optional[float] = Field(None, ge=0, le=20)

class ParseResult(BaseModel):
    """Compte-rendu global du parsing d'un fichier."""
    succes: List[EvaluationImportDTO] = []
    erreurs: List[ValidationErreurDTO] = []
    
    @property
    def total_lignes(self) -> int:
        return len(self.succes) + len(self.erreurs)
        
    @property
    def nb_succes(self) -> int:
        return len(self.succes)
        
    @property
    def nb_erreurs(self) -> int:
        return len(self.erreurs)
