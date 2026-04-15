from datetime import date
from domain.entities.etudiant import Etudiant

def get_etudiants_test():
    """Génère une liste d'étudiants pour les tests d'intégration."""
    return [
        Etudiant(id="ETU001", nom="DIALLO", prenom="Mamadou", matricule="2025001", date_naissance=date(2003, 5, 12)),
        Etudiant(id="ETU002", nom="NGUEMA", prenom="Jean-Paul", matricule="2025002", date_naissance=date(2002, 8, 20)),
        Etudiant(id="ETU003", nom="ZUE", prenom="Syntia", matricule="2025003", date_naissance=date(2004, 1, 30)),
        # ... on peut en ajouter d'autres dynamiquement si besoin
    ]
