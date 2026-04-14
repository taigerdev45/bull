from typing import List, Dict
from domain.services.interfaces.i_calculateur import ICalculateur
from domain.value_objects.note import Note
from domain.value_objects.moyenne import Moyenne, TypeCalculMoyenne
from domain.entities.evaluation import TypeEvaluation
from infrastructure.config.constants import PONDERATION_CC, PONDERATION_EXAMEN, PENALITE_PAR_HEURE

class CalculateurMatiere(ICalculateur):
    """Calculateur de la moyenne pour une matière spécifique."""

    def calculer(self, data: Dict) -> Moyenne:
        """
        data: {
            'evaluations': List[Evaluation],
            'heures_absence': int
        }
        """
        evals = data.get('evaluations', [])
        heures_abs = data.get('heures_absence', 0)
        
        if not evals:
            return Moyenne(0.0, TypeCalculMoyenne.ARITHMETIQUE, {"error": "Aucune évaluation"})

        # 1. Vérifier la présence d'un rattrapage
        rattrapage = next((e for e in evals if e.type == TypeEvaluation.RATTRAPAGE), None)
        if rattrapage and rattrapage.note_valeur is not None:
            valeur_base = rattrapage.note_valeur
            details = {"mode": "RATTRAPAGE"}
        else:
            # 2. CC x 40% + Examen x 60%
            cc = next((e for e in evals if e.type == TypeEvaluation.CC), None)
            examen = next((e for e in evals if e.type == TypeEvaluation.EXAMEN), None)
            
            if cc and examen and cc.note_valeur is not None and examen.note_valeur is not None:
                valeur_base = (cc.note_valeur * PONDERATION_CC) + (examen.note_valeur * PONDERATION_EXAMEN)
                details = {"cc": cc.note_valeur, "examen": examen.note_valeur, "mode": "PONDEREE"}
            elif len(evals) == 1:
                # Si une seule note (et pas de rattrapage géré au dessus)
                valeur_base = evals[0].note_valeur or 0.0
                details = {"mode": "UNIQUE", "note": valeur_base}
            else:
                # Moyenne arithmétique simple si structure incomplète
                notes = [e.note_valeur for e in evals if e.note_valeur is not None]
                valeur_base = sum(notes) / len(notes) if notes else 0.0
                details = {"mode": "ARITHMETIQUE_DEFAUT"}

        # 3. Pénalité absences (0.01 pt/heure)
        penalite = heures_abs * PENALITE_PAR_HEURE
        valeur_finale = max(0, valeur_base - penalite)
        
        details.update({
            "valeur_avant_penalite": valeur_base,
            "penalite_absences": penalite,
            "heures_absence": heures_abs
        })

        return Moyenne(valeur_finale, TypeCalculMoyenne.ARITHMETIQUE, details)

    def peut_calculer(self, data: Dict) -> bool:
        return 'evaluations' in data
