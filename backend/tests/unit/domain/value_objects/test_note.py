import pytest
from domain.value_objects.note import Note
from domain.exceptions.domain_exception import ValidationException

def test_note_creation_valide():
    n = Note(15.5)
    assert n.valeur == 15.5
    assert n.est_presente() is True

def test_note_limite_zero_valide():
    n = Note(0.0)
    assert n.valeur == 0
    assert n.est_presente() is True

def test_note_limite_vingt_valide():
    n = Note(20.0)
    assert n.valeur == 20
    assert n.est_presente() is True

def test_note_negative_leve_exception():
    with pytest.raises(ValidationException):
        Note(-1.0)

def test_note_trop_grande_leve_exception():
    with pytest.raises(ValidationException):
        Note(21.0)

def test_note_immutabilite():
    n = Note(10.0)
    with pytest.raises(AttributeError):
        n.valeur = 12.0

def test_appliquer_penalite_retourne_nouvelle_instance():
    n1 = Note(15.0)
    n2 = n1.appliquer_penalite(1.0)
    assert n1.valeur == 15.0
    assert n2.valeur == 14.0
    assert n1 is not n2

def test_penalite_ne_descend_pas_sous_zero():
    n = Note(0.5)
    n_finale = n.appliquer_penalite(1.0)
    assert n_finale.valeur == 0.0
