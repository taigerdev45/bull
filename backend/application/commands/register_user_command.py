from dataclasses import dataclass
from typing import Optional
from domain.repositories.i_etudiant_repository import IEtudiantRepository
from domain.repositories.i_enseignant_repository import IEnseignantRepository
from infrastructure.auth.firebase_auth_service import FirebaseAuthService
from domain.exceptions.domain_exception import ValidationException

@dataclass
class RegisterUserCommand:
    email: str
    password: str
    matricule: str
    role: str # 'etudiant' or 'enseignant'

class RegisterUserHandler:
    def __init__(self, etudiant_repo: IEtudiantRepository, 
                 enseignant_repo: IEnseignantRepository,
                 auth_service: FirebaseAuthService):
        self.etudiant_repo = etudiant_repo
        self.enseignant_repo = enseignant_repo
        self.auth_service = auth_service

    def handle(self, command: RegisterUserCommand) -> str:
        # 1. Récupération du dossier administratif
        if command.role == 'etudiant':
            record = self.etudiant_repo.get_by_matricule(command.matricule)
            role_label = "Étudiant"
        elif command.role == 'enseignant':
            record = self.enseignant_repo.get_by_matricule(command.matricule)
            role_label = "Enseignant"
        else:
            raise ValidationException("Rôle invalide pour l'auto-inscription.")

        # 2. Validations strictes
        if not record:
            raise ValidationException(f"Aucun dossier {role_label} trouvé pour le matricule {command.matricule}. Contactez le secrétariat.")
        
        if record.email.lower() != command.email.lower():
            raise ValidationException(f"L'email fourni ne correspond pas à l'email enregistré pour ce matricule.")

        if record.user_id:
            raise ValidationException("Ce matricule est déjà associé à un compte utilisateur.")

        # 3. Création du compte Firebase
        try:
            display_name = record.nom_complet
            user_id = self.auth_service.create_user(
                email=command.email,
                password=command.password,
                display_name=display_name
            )
            
            # 4. Attribution des rôles (Claims)
            self.auth_service.set_user_claims(user_id, command.role)
            
            # 5. Liaison technique
            record._user_id = user_id
            if command.role == 'etudiant':
                self.etudiant_repo.save(record)
            else:
                self.enseignant_repo.save(record)
                
            return user_id
            
        except Exception as e:
            # Rollback Firebase si possible ou log
            raise Exception(f"Erreur lors de l'inscription : {str(e)}")
