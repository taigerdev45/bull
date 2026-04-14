import pytest
from domain.services.orchestre_calcul import OrchestreCalcul
from domain.entities.evaluation import TypeEvaluation
from domain.value_objects.note import Note

@pytest.fixture
def orchestrateur():
    return OrchestreCalcul()

def test_cascade_calcul_matiere_ue_semestre(orchestrateur):
    """Vérifie que la cascade de calculs fonctionne correctement."""
    data = {
        'ues': [
            {
                'id': 'UE1',
                'credits': 6,
                'matieres': [
                    {
                        'id': 'M1', 
                        'coefficient': 2.0, 
                        'evaluations': [
                            # Note = 15
                            {'type': TypeEvaluation.EXAMEN, 'note_valeur': 15.0}
                        ],
                        'heures_absence': 0
                    }
                ]
            }
        ]
    }
    
    resultat = orchestrateur.calculer_bulletin_semestre("etud_1", 5, data)
    
    # 1. Vérification de la moyenne générale
    assert resultat['moyenne_generale'] == 15.0
    
    # 2. Vérification des crédits acquis (UE1 > 10 donc acquis)
    assert resultat['total_credits'] == 6
    
    # 3. Vérification de la structure du retour
    assert resultat['etudiant_id'] == "etud_1"
    assert len(resultat['details']) == 1
