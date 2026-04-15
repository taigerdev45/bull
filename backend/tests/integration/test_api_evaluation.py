import pytest
from rest_framework import status
from unittest.mock import patch, MagicMock

@pytest.mark.django_db
def test_post_evaluation_authentifie(api_client, ioc_container):
    """Vérifie qu'un POST valide crée une évaluation et déclenche l'orchestre."""
    # Mock de l'utilisateur authentifié
    user_mock = MagicMock()
    user_mock.is_authenticated = True
    user_mock.email = "enseignant@inptic.ga"
    
    # Payload
    data = {
        "etudiant_id": "ETU1",
        "matiere_id": "MAT1",
        "type": "CC",
        "note": 14.5
    }
    
    with patch('infrastructure.config.dependency_injection.Container', ioc_container):
        # On simule l'utilisateur sur la requête
        api_client.force_authenticate(user=user_mock)
        response = api_client.post('/api/evaluations/', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert ioc_container.evaluation_repo().creer.called
        # Vérifier que l'orchestrateur a été appelé pour le recalcul
        assert ioc_container.orchestre_calcul().calculer_tout_pour_etudiant.called

@pytest.mark.django_db
def test_post_evaluation_anonyme_refuse(api_client):
    data = {"etudiant_id": "ETU1", "matiere_id": "MAT1", "type": "CC", "note": 14.5}
    response = api_client.post('/api/evaluations/', data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN
