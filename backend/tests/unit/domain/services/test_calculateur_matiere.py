import pytest
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.entities.evaluation import Evaluation, TypeEvaluation
from domain.value_objects.note import Note

@pytest.fixture
def calculateur():
    return CalculateurMatiere()

def test_ponderation_standard(calculateur):
    evals = [
        Evaluation("e1", "m1", TypeEvaluation.CC, Note(10.0)),
        Evaluation("e1", "m1", TypeEvaluation.EXAMEN, Note(15.0))
    ]
    # CC(10)*0.4 + EXAM(15)*0.6 = 4 + 9 = 13
    moyenne = calculateur.calculer({'evaluations': evals})
    assert moyenne.valeur == 13.0
    assert moyenne.details['mode'] == "PONDEREE"

def test_rattrapage_remplace_tout(calculateur):
    evals = [
        Evaluation("e1", "m1", TypeEvaluation.CC, Note(10.0)),
        Evaluation("e1", "m1", TypeEvaluation.EXAMEN, Note(8.0)),
        Evaluation("e1", "m1", TypeEvaluation.RATTRAPAGE, Note(12.0))
    ]
    moyenne = calculateur.calculer({'evaluations': evals})
    assert moyenne.valeur == 12.0
    assert moyenne.details['mode'] == "RATTRAPAGE"

def test_penalite_absences_appliquee(calculateur):
    evals = [Evaluation("e1", "m1", TypeEvaluation.EXAMEN, Note(10.0))]
    # 10 notes, 100 heures d'absence x 0.01 = -1pt
    moyenne = calculateur.calculer({'evaluations': evals, 'heures_absence': 100})
    assert moyenne.valeur == 9.0
    assert moyenne.details['penalite_absences'] == 1.0

def test_seule_note_prise_telle_quelle(calculateur):
    evals = [Evaluation("e1", "m1", TypeEvaluation.CC, Note(14.0))]
    moyenne = calculateur.calculer({'evaluations': evals})
    assert moyenne.valeur == 14.0
    assert moyenne.details['mode'] == "UNIQUE"
