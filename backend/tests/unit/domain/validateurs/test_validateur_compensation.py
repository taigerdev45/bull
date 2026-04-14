import pytest
from domain.services.validateurs.validateur_compensation import ValidateurCompensation
from domain.value_objects.validation_result import EtatAcquisition

@pytest.fixture
def validateur():
    return ValidateurCompensation()

def test_acquisition_directe_si_ue_sup_10(validateur):
    res = validateur.valider({
        'moyenne_ue': 10.5,
        'moyenne_generale_semestre': 8.0,
        'credits_ue': 6
    })
    assert res.etat == EtatAcquisition.ACQUISE_DIRECTE
    assert res.credits_acquis == 6

def test_compensation_autorisee_si_generale_sup_10(validateur):
    # UE à 9.5 mais Semestre à 10.2 -> Compensée
    res = validateur.valider({
        'moyenne_ue': 9.5,
        'moyenne_generale_semestre': 10.2,
        'credits_ue': 6
    })
    assert res.etat == EtatAcquisition.COMPENSEE
    assert res.credits_acquis == 6

def test_non_acquise_si_les_deux_inf_10(validateur):
    res = validateur.valider({
        'moyenne_ue': 9.5,
        'moyenne_generale_semestre': 9.8,
        'credits_ue': 6
    })
    assert res.etat == EtatAcquisition.NON_ACQUISE
    assert res.credits_acquis == 0
