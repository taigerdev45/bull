import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infrastructure.config.settings')
django.setup()

from infrastructure.persistence.django_models.models import EnseignantModel, MatiereModel
from infrastructure.config.dependency_injection import Container

def fix_modou():
    auth_service = Container.auth_service()
    
    email = "modou@sylla.test"
    password = "87654321"
    
    print(f"Checking user {email} in Firebase...")
    user_id = None
    existing_user = auth_service.get_user_by_email(email)
    
    if existing_user:
        user_id = existing_user['uid']
        print(f"User exists: {user_id}")
    else:
        print("Creating user in Firebase...")
        user_id = auth_service.create_user(
            email=email,
            password=password,
            display_name="Modou SYLLA"
        )
        print(f"User created: {user_id}")
    
    auth_service.set_user_claims(user_id, 'enseignant')
    
    print("Linking to EnseignantModel...")
    try:
        e = EnseignantModel.objects.get(matricule='ENS-ENS-TEST-100')
        e.user_id = user_id
        e.save()
        print("Model updated.")
        
        # Assign matieres
        # 1. Mathematique appliques (already assigned likely, but re-confirm)
        # 2. Raccourci clavier
        m1 = MatiereModel.objects.get(libelle="Mathematique appliques")
        m1.enseignant = e
        m1.save()
        
        m2 = MatiereModel.objects.get(libelle="Raccourci clavier")
        m2.enseignant = e
        m2.save()
        
        print("Matieres assigned.")
    except Exception as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    fix_modou()
