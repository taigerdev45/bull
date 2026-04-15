import pytest
from domain.services.validateurs.validateur_compensation import ValidateurCompensation
from domain.value_objects.moyenne import Moyenne, TypeCalculMoyenne

@pytest.fixture
def validateur():
    return ValidateurCompensation(credits_ue=12)

def test_acquisition_directe(validateur):
    moy_ue = Moyenne(10.0, TypeCalculMoyenne.NORMAL)
    moy_gen = Moyenne(8.0, TypeCalculMoyenne.NORMAL)
    res = validateur.valider(moy_ue, moy_gen)
    assert res.est_valide is True
    assert res.statut == 'ACQUISE_DIRECTE'
    assert res.credits_acquis == 12

def test_compensation_autorisee(validateur):
    moy_ue = Moyenne(9.0, TypeCalculMoyenne.NORMAL)
    moy_gen = Moyenne(10.5, TypeCalculMoyenne.NORMAL)
    res = validateur.valider(moy_ue, moy_gen)
    assert res.est_valide is True
    assert res.statut == 'COMPENSEE'
    assert res.credits_acquis == 12

def test_non_acquise(validateur):
    moy_ue = Moyenne(8.0, TypeCalculMoyenne.NORMAL)
    moy_gen = Moyenne(9.5, TypeCalculMoyenne.NORMAL)
    res = validateur.valider(moy_ue, moy_gen)
    assert res.est_valide is False
    assert res.statut == 'NON_ACQUISE'
    assert res.credits_acquis == 0
