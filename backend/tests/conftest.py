import pytest
from unittest.mock import MagicMock
import firebase_admin

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
def etudiant_repo_mock():
    return MagicMock()

@pytest.fixture
def evaluation_repo_mock():
    return MagicMock()
