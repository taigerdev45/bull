from domain.entities.ue import UE
from domain.entities.matiere import Matiere
from domain.value_objects.coefficient import Coefficient

def get_referentiel_lp_asur():
    """Retourne une structure simplifiée du référentiel ASUR pour les tests."""
    ue_securite = UE(code="UE6-1", libelle="Sécurité Réseaux", credits=15, semestre=6)
    
    m1 = Matiere(libelle="Cryptographie", coefficient=Coefficient(2.0), credits=3, ue_id="UE6-1")
    m2 = Matiere(libelle="Pare-feu", coefficient=Coefficient(3.0), credits=5, ue_id="UE6-1")
    
    return {
        "ues": [ue_securite],
        "matieres": [m1, m2]
    }
