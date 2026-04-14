from typing import Dict, List
from enum import Enum, auto

class DecisionJury(Enum):
    DIPLOME = auto()
    REPRISE_SOUTENANCE = auto()
    REDOUBLEMENT = auto()

class DecideurJury:
    """Service de prise de décision finale du jury d'examen."""

    def determiner_decision(self, data: Dict) -> DecisionJury:
        """
        data: {
            'total_credits': int,
            'ue_echouees_critiques': List[str],
            'moyenne_annuelle': float
        }
        """
        credits = data.get('total_credits', 0)
        echouees = data.get('ue_echouees_critiques', [])
        
        if credits >= 60:
            return DecisionJury.DIPLOME
            
        # Cas de la reprise de soutenance (Paramétrable)
        # S'il ne manque que l'UE6-2 (ou une liste critique) et que les crédits sont suffisants par ailleurs
        if credits >= 50 and len(echouees) == 1 and "UE6-2" in echouees:
            return DecisionJury.REPRISE_SOUTENANCE

        return DecisionJury.REDOUBLEMENT
