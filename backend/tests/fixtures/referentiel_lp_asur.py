from domain.entities.ue import UE
from domain.entities.matiere import Matiere
from domain.value_objects.coefficient import Coefficient

def get_referentiel_test():
    """Retourne un dictionnaire des entités du référentiel pour les tests."""
    
    # UE 5-1: Réseaux et Télécoms (Exemple)
    ue51 = UE(code="UE5-1", libelle="Réseaux et Télécoms", credits=12, semestre=5)
    
    m1 = Matiere(libelle="Architecture des réseaux", coefficient=Coefficient(3.0), credits=4, ue_id="UE5-1")
    m2 = Matiere(libelle="Services IP", coefficient=Coefficient(2.0), credits=4, ue_id="UE5-1")
    m3 = Matiere(libelle="Téléphonie IP", coefficient=Coefficient(2.0), credits=4, ue_id="UE5-1")
    
    # UE 6-2: Stage & Projet (UE Critique pour Soutenance)
    ue62 = UE(code="UE6-2", libelle="Stage et Projet Professionnel", credits=20, semestre=6)
    m4 = Matiere(libelle="Stage", coefficient=Coefficient(5.0), credits=15, ue_id="UE6-2")
    m5 = Matiere(libelle="Projet", coefficient=Coefficient(2.0), credits=5, ue_id="UE6-2")

    return {
        "ues": [ue51, ue62],
        "matieres": [m1, m2, m3, m4, m5]
    }
