from pydantic import BaseModel
from typing import Optional, Any

class ValidationErreurDTO(BaseModel):
    """Représente une erreur détectée lors du parsing Excel."""
    ligne: int
    colonne: str
    valeur: Optional[Any] = None
    message: str
    type_erreur: str # VALIDATION, NOT_FOUND, FORMAT, DOMAIN
