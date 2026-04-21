import firebase_admin
from firebase_admin import auth
from typing import Dict, Any, Optional

class FirebaseAuthService:
    """Service pour gérer l'authentification Firebase (Admin SDK)."""

    def create_user(self, email: str, password: str, display_name: str) -> str:
        """
        Crée un utilisateur dans Firebase Auth.
        Retourne l'UID Firebase.
        """
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            return user.uid
        except Exception as e:
            raise Exception(f"Erreur lors de la création de l'utilisateur Firebase: {str(e)}")

    def set_user_claims(self, uid: str, role: str):
        """
        Définit les custom claims (rôles) pour l'utilisateur.
        """
        try:
            auth.set_custom_user_claims(uid, {'role': role})
        except Exception as e:
            raise Exception(f"Erreur lors de la définition des rôles Firebase: {str(e)}")

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Récupère les informations d'un utilisateur par son email.
        """
        try:
            user = auth.get_user_by_email(email)
            return {
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name,
                'claims': user.custom_claims
            }
        except auth.UserNotFoundError:
            return None
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de l'utilisateur: {str(e)}")

    def delete_user(self, uid: str):
        """Supprime un utilisateur Firebase."""
        auth.delete_user(uid)
