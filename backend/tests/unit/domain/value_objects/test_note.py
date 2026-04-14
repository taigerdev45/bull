import pytest
from domain.value_objects.note import Note
from domain.exceptions.domain_exception import NoteInvalideException

def test_creation_note_valide():
    note = Note(15.5)
    assert note.valeur == 15.5
    assert str(note) == "15.50/20"

def test_note_trop_grande_leve_exception():
    with pytest.raises(NoteInvalideException):
        Note(21.0)

def test_note_negative_leve_exception():
    with pytest.raises(NoteInvalideException):
        Note(-1.0)

def test_immutabilite_note():
    note = Note(10.0)
    with pytest.raises(AttributeError):
        note.valeur = 12.0

def test_appliquer_penalite_retourne_nouvelle_instance():
    note_initiale = Note(15.0)
    nouvelle_note = note_initiale.appliquer_penalite(2.0)
    
    assert nouvelle_note.valeur == 13.0
    assert note_initiale.valeur == 15.0  # L'original n'a pas changé
    assert nouvelle_note is not note_initiale

def test_penalite_plancher_zero():
    note = Note(1.0)
    resultat = note.appliquer_penalite(5.0)
    assert resultat.valeur == 0.0
