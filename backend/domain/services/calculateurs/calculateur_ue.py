from typing import Dict
from domain.services.interfaces.i_calculateur import ICalculateur
from domain.value_objects.moyenne import Moyenne, TypeCalculMoyenne

class CalculateurUE(ICalculateur):
    """Calculateur de la moyenne d'une UE par pondération des matières."""

    def calculer(self, data: Dict) -> Moyenne:
        """
        data: {
            'moyennes_matieres': Dict[str, Moyenne],
            'coefficients_matieres': Dict[str, float]
        }
        """
        moyennes = data.get('moyennes_matieres', {})
        coefficients = data.get('coefficients_matieres', {})
        
        total_poids = 0.0
        somme_ponderee = 0.0
        
        for m_id, moyenne in moyennes.items():
            coeff = coefficients.get(m_id, 1.0)
            somme_ponderee += moyenne.valeur * coeff
            total_poids += coeff
            
        if total_poids == 0:
            return Moyenne(0.0, TypeCalculMoyenne.PONDEREE, {"error": "Aucun coefficient trouvé"})
            
        valeur_ue = somme_ponderee / total_poids
        return Moyenne(valeur_ue, TypeCalculMoyenne.PONDEREE, {"total_poids": total_poids})

    def peut_calculer(self, data: Dict) -> bool:
        return 'moyennes_matieres' in data
