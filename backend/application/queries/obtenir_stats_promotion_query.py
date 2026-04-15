from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ObtenirStatsPromotionQuery:
    """Requête pour les statistiques globales d'une promo."""
    promotion_id: str
    semestre: Optional[int] = None
    ue_id: Optional[str] = None
    matiere_id: Optional[str] = None
