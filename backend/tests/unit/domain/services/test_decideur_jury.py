import pytest
from domain.services.decideurs.decideur_jury import DecideurJury, DecisionJury

@pytest.fixture
def decideur():
    return DecideurJury()

def test_diplome_60_credits_acquis(decideur):
    decision = decideur.determiner_decision({
        'total_credits': 60,
        'ue_echouees_critiques': []
    })
    assert decision == DecisionJury.DIPLOME

def test_reprise_soutenance_si_uniquement_ue62_manquante(decideur):
    decision = decideur.determiner_decision({
        'total_credits': 52,
        'ue_echouees_critiques': ["UE6-2"]
    })
    assert decision == DecisionJury.REPRISE_SOUTENANCE

def test_redoublement_si_credits_insuffisants(decideur):
    decision = decideur.determiner_decision({
        'total_credits': 45,
        'ue_echouees_critiques': ["UE6-1", "UE6-2"]
    })
    assert decision == DecisionJury.REDOUBLEMENT
