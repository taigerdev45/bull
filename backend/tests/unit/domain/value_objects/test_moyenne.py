import pytest
from domain.value_objects.moyenne import Moyenne, TypeCalculMoyenne

def test_moyenne_reussite_exact_10():
    m = Moyenne(10.0, TypeCalculMoyenne.NORMAL)
    assert m.est_reussite(10.0) is True

def test_moyenne_reussite_superieur_10():
    m = Moyenne(10.1, TypeCalculMoyenne.NORMAL)
    assert m.est_reussite(10.0) is True

def test_moyenne_echec_inferieur_10():
    m = Moyenne(9.9, TypeCalculMoyenne.NORMAL)
    assert m.est_reussite(10.0) is False

def test_moyenne_details_immutabilite():
    m = Moyenne(12.0, TypeCalculMoyenne.NORMAL, {"test": 1})
    with pytest.raises(AttributeError):
        m.valeur = 13.0
