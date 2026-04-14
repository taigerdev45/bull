from typing import Dict
from domain.services.interfaces.i_calculateur import ICalculateur
from domain.value_objects.moyenne import Moyenne, TypeCalculMoyenne
from domain.value_objects.mention import Mention  # Assumons que c'est une Enum
from infrastructure.config.constants import (
    MENTION_PASSABLE, MENTION_ASSEZ_BIEN, MENTION_BIEN, MENTION_TRES_BIEN
)

class CalculateurAnnuel(ICalculateur):
    """Calculateur de la moyenne annuelle et détermination de la mention."""

    def calculer(self, data: Dict) -> Moyenne:
        """
        data: {
            'moyenne_s1': float,
            'moyenne_s2': float
        }
        """
        m1 = data.get('moyenne_s1', 0.0)
        m2 = data.get('moyenne_s2', 0.0)
        
        moyenne_annuelle = (m1 + m2) / 2
        
        mention = self._determiner_mention(moyenne_annuelle)
        
        return Moyenne(moyenne_annuelle, TypeCalculMoyenne.ARITHMETIQUE, {"mention": mention})

    def _determiner_mention(self, moyenne: float) -> str:
        if moyenne >= MENTION_TRES_BIEN: return "Très Bien"
        if moyenne >= MENTION_BIEN: return "Bien"
        if moyenne >= MENTION_ASSEZ_BIEN: return "Assez Bien"
        if moyenne >= MENTION_PASSABLE: return "Passable"
        return "Ajourné"

    def peut_calculer(self, data: Dict) -> bool:
        return 'moyenne_s1' in data and 'moyenne_s2' in data
