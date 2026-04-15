from dataclasses import dataclass
from typing import Tuple
from ...value_objects.moyenne import Moyenne

@dataclass(frozen=True)
class ValidationResult:
    """Value Object résultat validation"""
    est_valide: bool
    statut: str  # 'ACQUISE_DIRECTE', 'COMPENSEE', 'NON_ACQUISE'
    credits_acquis: int
    message: str

class ValidateurCompensation:
    """
    Pattern Chain of Responsibility + Strategy.
    Valide une UE selon règles de compensation.
    """
    
    SEUIL_REUSSITE = 10.0
    
    def __init__(self, credits_ue: int):
        self._credits_ue = credits_ue
    
    def valider(self, moyenne_ue: Moyenne, moyenne_generale: Moyenne) -> ValidationResult:
        """
        Chaîne de décision:
        1. Acquisition directe (moyenne UE >= 10)
        2. Compensation (moyenne UE < 10 mais générale >= 10)
        3. Non acquise
        """
        # Étape 1: Acquisition directe
        if moyenne_ue.est_reussite(self.SEUIL_REUSSITE):
            return ValidationResult(
                est_valide=True,
                statut='ACQUISE_DIRECTE',
                credits_acquis=self._credits_ue,
                message=f"UE acquise directement (moyenne: {moyenne_ue.valeur:.2f})"
            )
        
        # Étape 2: Compensation
        if moyenne_generale.est_reussite(self.SEUIL_REUSSITE):
            return ValidationResult(
                est_valide=True,
                statut='COMPENSEE',
                credits_acquis=self._credits_ue,  # Tous les crédits quand même!
                message=f"UE acquise par compensation (UE: {moyenne_ue.valeur:.2f}, générale: {moyenne_generale.valeur:.2f})"
            )
        
        # Étape 3: Non acquise
        return ValidationResult(
            est_valide=False,
            statut='NON_ACQUISE',
            credits_acquis=0,
            message=f"UE non acquise (moyenne: {moyenne_ue.valeur:.2f})"
        )
