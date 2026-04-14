from domain.entities.etudiant import Etudiant
from datetime import date

def get_etudiants_jeu_essai():
    """Génère un portefeuille d'étudiants pour les tests d'intégration."""
    return [
        Etudiant("KOUAKOU", "Jean", "INP001", date(2000, 1, 1), id="e1"),
        Etudiant("TRAORE", "Fatou", "INP002", date(2001, 5, 20), id="e2"),
        Etudiant("DIALLO", "Amadou", "INP003", date(1999, 12, 10), id="e3"),
        # ... on pourrait en ajouter plus ici pour atteindre 24
    ]
