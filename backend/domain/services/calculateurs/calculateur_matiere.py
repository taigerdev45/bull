from typing import Dict, Any, List
from domain.services.interfaces.i_calculateur import ICalculateur
from domain.services.interfaces.i_penalite_service import IPenaliteService
from ...value_objects.note import Note
from ...value_objects.moyenne import Moyenne, TypeCalculMoyenne
from ...entities.evaluation import TypeEvaluation
from domain.exceptions.domain_exception import CalculImpossibleException

class CalculateurMatiere(ICalculateur):
    """
    Calcule la moyenne d'une matière selon règles métier.
    Pattern Strategy: algorithme interchangeable.
    """
    
    PONDERATION_CC = 0.4
    PONDERATION_EXAMEN = 0.6
    
    def __init__(self, penalite_service: 'IPenaliteService'):
        # Injection dépendance
        self._penalite_service = penalite_service
    
    def peut_calculer(self, contexte: Dict[str, Any]) -> bool:
        evaluations = contexte.get('evaluations', [])
        return len(evaluations) > 0
    
    def calculer(self, contexte: Dict[str, Any]) -> Moyenne:
        """
        Algorithme:
        1. Si rattrapage présent → rattrapage remplace tout
        2. Sinon pondération 40/60 CC/Examen
        3. Appliquer pénalités absences
        """
        evaluations: List = contexte['evaluations']
        etudiant_id = contexte['etudiant_id']
        matiere_id = contexte['matiere_id']
        
        # Stratégie selon présence rattrapage
        rattrapage = self._trouver_evaluation(evaluations, TypeEvaluation.RATTRAPAGE)
        
        if rattrapage and rattrapage.note.est_presente():
            return self._calcul_avec_rattrapage(rattrapage, etudiant_id, matiere_id)
        
        return self._calcul_normal(evaluations, etudiant_id, matiere_id)
    
    def _trouver_evaluation(self, evaluations: List, type_eval: TypeEvaluation):
        return next((e for e in evaluations if e.type == type_eval), None)
    
    def _calcul_avec_rattrapage(self, rattrapage, etudiant_id, matiere_id) -> Moyenne:
        note = rattrapage.note
        note_penalisee = self._appliquer_penalite(note, etudiant_id, matiere_id)
        
        return Moyenne(
            valeur=float(note_penalisee.valeur) if note_penalisee.valeur is not None else 0.0,
            type_calcul=TypeCalculMoyenne.RATTRAPAGE,
            details={
                'note_rattrapage': float(rattrapage.note.valeur) if rattrapage.note.valeur is not None else 0.0,
                'penalite': (float(rattrapage.note.valeur) - float(note_penalisee.valeur)) if (rattrapage.note.valeur and note_penalisee.valeur) else 0.0,
                'methode': 'Rattrapage remplace tout'
            }
        )
    
    def _calcul_normal(self, evaluations, etudiant_id, matiere_id) -> Moyenne:
        cc = self._trouver_evaluation(evaluations, TypeEvaluation.CC)
        examen = self._trouver_evaluation(evaluations, TypeEvaluation.EXAMEN)
        
        note_cc = cc.note if cc else Note(None)
        note_examen = examen.note if examen else Note(None)
        
        # Calcul pondéré
        if note_cc.est_presente() and note_examen.est_presente():
            valeur = (float(note_cc.valeur) * self.PONDERATION_CC + 
                     float(note_examen.valeur) * self.PONDERATION_EXAMEN)
            type_calc = TypeCalculMoyenne.NORMAL
        elif note_cc.est_presente():
            valeur = float(note_cc.valeur)
            type_calc = TypeCalculMoyenne.UNIQUE
        elif note_examen.est_presente():
            valeur = float(note_examen.valeur)
            type_calc = TypeCalculMoyenne.UNIQUE
        else:
            raise CalculImpossibleException("Aucune note disponible")
        
        # Appliquer pénalités
        note_finale = self._appliquer_penalite(Note(valeur), etudiant_id, matiere_id)
        
        return Moyenne(
            valeur=float(note_finale.valeur) if note_finale.valeur is not None else 0.0,
            type_calcul=type_calc,
            details={
                'note_cc': float(note_cc.valeur) if note_cc.est_presente() else None,
                'note_examen': float(note_examen.valeur) if note_examen.est_presente() else None,
                'ponderation_cc': self.PONDERATION_CC if type_calc == TypeCalculMoyenne.NORMAL else None,
                'methode': 'Pondération 40/60' if type_calc == TypeCalculMoyenne.NORMAL else 'Note unique'
            }
        )
    
    def _appliquer_penalite(self, note: Note, etudiant_id: str, matiere_id: str) -> Note:
        penalite = self._penalite_service.calculer(etudiant_id, matiere_id)
        return note.appliquer_penalite(penalite)
