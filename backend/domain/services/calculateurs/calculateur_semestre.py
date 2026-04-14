from typing import List, Dict
from domain.services.interfaces.i_calculateur import ICalculateur
from domain.value_objects.moyenne import Moyenne, TypeCalculMoyenne
from domain.value_objects.validation_result import ValidationResult, EtatAcquisition
from infrastructure.config.constants import CREDITS_SEMESTRE

class CalculateurSemestre(ICalculateur):
    """Calculateur de la moyenne semestrielle et agrégation des crédits."""

    def calculer(self, data: Dict) -> Moyenne:
        """
        data: {
            'moyennes_ue': List[Moyenne],
            'coefficients_ue': List[float] (souvent 1.0 par défaut pour les UE)
        }
        """
        moyennes = data.get('moyennes_ue', [])
        
        if not moyennes:
            return Moyenne(0.0, TypeCalculMoyenne.ARITHMETIQUE, {"error": "Aucune UE trouvée"})
            
        valeur_moyenne = sum(m.valeur for m in moyennes) / len(moyennes)
        return Moyenne(valeur_moyenne, TypeCalculMoyenne.ARITHMETIQUE, {"nb_ue": len(moyennes)})

    def peut_calculer(self, data: Dict) -> bool:
        return 'moyennes_ue' in data
