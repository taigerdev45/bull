import pytest
from rest_framework import status
from unittest.mock import patch, MagicMock
from io import BytesIO
import openpyxl

@pytest.mark.django_db
def test_post_import_excel_valide(api_client, ioc_container):
    """Vérifie l'importation d'un fichier Excel via API."""
    # 1. Créer un fichier Excel factice en mémoire
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Matricule", "Nom", "Prénom", "Matière", "CC", "Examen", "Rattrapage"])
    ws.append(["2025001", "DIALLO", "Mamadou", "Architecture des réseaux", 12, 14, None])
    
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    
    # 2. Mocker les résolutions de repositories
    mock_etudiant = MagicMock()
    mock_etudiant.id = "ETU1"
    ioc_container.etudiant_repo().get_by_matricule.return_value = mock_etudiant
    
    mock_matiere = MagicMock()
    mock_matiere.id = "MAT1"
    ioc_container.matiere_repo().get_by_libelle.return_value = mock_matiere

    # 3. Appel API
    with patch('infrastructure.config.dependency_injection.Container', ioc_container):
        api_client.force_authenticate(user=MagicMock())
        response = api_client.post(
            '/api/import/evaluations/', 
            {'fichier': buffer}, 
            format='multipart'
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert ioc_container.evaluation_repo().bulk_creer.called
        assert response.data['importation']['succes'] > 0
