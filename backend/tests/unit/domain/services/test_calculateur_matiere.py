import pytest
from unittest.mock import MagicMock
from domain.services.calculateurs.calculateur_matiere import CalculateurMatiere
from domain.entities.evaluation import Evaluation, TypeEvaluation, Note
from domain.exceptions.domain_exception import CalculImpossibleException

@pytest.fixture
def mock_penalite_service():
    service = MagicMock()
    service.calculer.return_value = 0.0
    return service

@pytest.fixture
def calculateur(mock_penalite_service):
    return CalculateurMatiere(mock_penalite_service)

def test_ponderation_40_60(calculateur):
    contexte = {
        'etudiant_id': 'E1',
        'matiere_id': 'M1',
        'evaluations': [
            Evaluation('E1', 'M1', TypeEvaluation.CC, Note(10.0)),
            Evaluation('E1', 'M1', TypeEvaluation.EXAMEN, Note(12.0))
        ]
    }
    moyenne = calculateur.calculer(contexte)
    # (10 * 0.4) + (12 * 0.6) = 4 + 7.2 = 11.2
    assert moyenne.valeur == 11.2

def test_rattrapage_remplace_tout(calculateur):
    contexte = {
        'etudiant_id': 'E1',
        'matiere_id': 'M1',
        'evaluations': [
            Evaluation('E1', 'M1', TypeEvaluation.CC, Note(10.0)),
            Evaluation('E1', 'M1', TypeEvaluation.EXAMEN, Note(8.0)),
            Evaluation('E1', 'M1', TypeEvaluation.RATTRAPAGE, Note(13.0))
        ]
    }
    moyenne = calculateur.calculer(contexte)
    assert moyenne.valeur == 13.0

def test_penalite_absences_appliquee(calculateur, mock_penalite_service):
    mock_penalite_service.calculer.return_value = 1.5
    contexte = {
        'etudiant_id': 'E1',
        'matiere_id': 'M1',
        'evaluations': [
            Evaluation('E1', 'M1', TypeEvaluation.EXAMEN, Note(15.0))
        ]
    }
    moyenne = calculateur.calculer(contexte)
    assert moyenne.valeur == 13.5

def test_aucune_note_leve_exception(calculateur):
    contexte = {'etudiant_id': 'E1', 'matiere_id': 'M1', 'evaluations': []}
    with pytest.raises(CalculImpossibleException):
        calculateur.calculer(contexte)
