import os
import django
import sys
from unittest.mock import MagicMock

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.config.settings')
django.setup()

from interfaces.api.views.ue_viewset import UEViewSet
from infrastructure.persistence.django_models.models import EnseignantModel

def test_ue_list_teacher():
    viewset = UEViewSet()
    request = MagicMock()
    
    # Simulate a teacher user
    # Modou SYLLA's UID from my previous check was whatever Firebase gave
    # I'll find it from the DB
    try:
        e = EnseignantModel.objects.get(matricule='ENS-ENS-TEST-100')
        print(f"Testing for teacher: {e.prenom} {e.nom}, UID: {e.user_id}")
        
        request.user.username = e.user_id
        request.user.uid = e.user_id
        request.user.role = 'enseignant'
        request.user.is_authenticated = True
        request.user.is_staff = False
        
        response = viewset.list(request)
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Data: {response.data}")
    except Exception as err:
        print(f"Crash: {err}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ue_list_teacher()
