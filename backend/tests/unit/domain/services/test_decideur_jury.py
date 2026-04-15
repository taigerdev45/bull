import pytest
from domain.services.decideurs.decideur_jury import DecideurJury, DecisionJury

@pytest.fixture
def decideur():
    return DecideurJury()

def test_decision_diplome(decideur):
    data = {'total_credits': 60, 'ue_echouees_critiques': [], 'moyenne_annuelle': 12.5}
    assert decideur.determiner_decision(data) == DecisionJury.DIPLOME

def test_decision_reprise_soutenance(decideur):
    # Manque seulement l'UE6-2 (Stage/Projet)
    data = {'total_credits': 55, 'ue_echouees_critiques': ["UE6-2"], 'moyenne_annuelle': 11.0}
    assert decideur.determiner_decision(data) == DecisionJury.REPRISE_SOUTENANCE

def test_decision_redoublement_credits_insuffisants(decideur):
    data = {'total_credits': 45, 'ue_echouees_critiques': ["UE5-1", "UE6-1"], 'moyenne_annuelle': 9.5}
    assert decideur.determiner_decision(data) == DecisionJury.REDOUBLEMENT
