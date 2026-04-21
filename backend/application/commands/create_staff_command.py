from dataclasses import dataclass
from domain.entities.personnel import Personnel
from domain.repositories.i_personnel_repository import IPersonnelRepository
from infrastructure.auth.supabase_auth_service import SupabaseAuthService
from domain.exceptions.domain_exception import ValidationException

@dataclass
class CreateStaffCommand:
    nom: str
    prenom: str
    email: str
    password: str
    role: str # 'admin' or 'secretariat'

class CreateStaffHandler:
    def __init__(self, personnel_repo: IPersonnelRepository, 
                 auth_service: SupabaseAuthService):
        self.personnel_repo = personnel_repo
        self.auth_service = auth_service

    def handle(self, command: CreateStaffCommand) -> str:
        # 1. Vérification si déjà existant
        existing = self.personnel_repo.get_by_email(command.email)
        if existing:
            raise ValidationException("Un membre du personnel avec cet email existe déjà.")

        # 2. Création Firebase
        try:
            display_name = f"{command.prenom} {command.nom}"
            user_id = self.auth_service.create_user(
                email=command.email,
                password=command.password,
                display_name=display_name
            )
            
            # 3. Attribution des rôles
            self.auth_service.set_user_claims(user_id, command.role)
            
            # 4. Enregistrement dans le domaine
            personnel = Personnel(
                nom=command.nom,
                prenom=command.prenom,
                email=command.email,
                role=command.role,
                user_id=user_id
            )
            self.personnel_repo.save(personnel)
            
            return user_id
            
        except Exception as e:
            raise Exception(f"Erreur lors de la création du personnel : {str(e)}")
