import pytest
from unittest.mock import MagicMock
from rest_framework.test import APIClient
from infrastructure.config.dependency_injection import Container

@pytest.fixture(autouse=True)
def mock_firebase(monkeypatch):
    """Fixture automatique pour mocker Firebase Admin SDK durant tous les tests."""
    mock_app = MagicMock()
    mock_db = MagicMock()
    
    # Mock firebase_admin methods
    monkeypatch.setattr("firebase_admin.initialize_app", lambda *args, **kwargs: mock_app)
    monkeypatch.setattr("firebase_admin.credentials.Certificate", lambda *args, **kwargs: MagicMock())
    
    # Mock firestore client
    monkeypatch.setattr("google.cloud.firestore.Client", lambda *args, **kwargs: mock_db)
    
    return mock_db

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def etudiant_repo_mock():
    return MagicMock()

@pytest.fixture
def evaluation_repo_mock():
    return MagicMock()

@pytest.fixture
def matiere_repo_mock():
    return MagicMock()

@pytest.fixture
def ue_repo_mock():
    return MagicMock()

@pytest.fixture
def resultat_repo_mock():
    return MagicMock()

@pytest.fixture
def ioc_container(etudiant_repo_mock, evaluation_repo_mock, matiere_repo_mock, ue_repo_mock, resultat_repo_mock):
    """Conteneur IoC avec des mocks pour les tests unitaires/intégration."""
    container = Container()
    container.etudiant_repo.override(etudiant_repo_mock)
    container.evaluation_repo.override(evaluation_repo_mock)
    container.matiere_repo.override(matiere_repo_mock)
    container.ue_repo.override(ue_repo_mock)
    container.resultat_repo.override(resultat_repo_mock)
    return container
