from supabase import create_client, Client
from typing import Dict, Any, Optional
import os

class SupabaseAuthService:
    """Service pour gérer l'authentification Supabase (GoTrue Admin SDK)."""

    def __init__(self):
        url: str = os.getenv("SUPABASE_URL", "")
        key: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "") # Utilise la service_role key pour les actions admin
        if not url or not key:
            # On ne lève pas d'exception ici pour permettre le démarrage de l'app si non configuré
            self.client = None
        else:
            self.client: Client = create_client(url, key)

    def create_user(self, email: str, password: str, display_name: str) -> str:
        """
        Crée un utilisateur dans Supabase Auth via l'API Admin.
        """
        if not self.client:
            raise Exception("Supabase non configuré.")
            
        try:
            # Création via le SDK Admin (nécessite la service_role key)
            res = self.client.auth.admin.create_user({
                "email": email,
                "password": password,
                "user_metadata": {"display_name": display_name},
                "email_confirm": True
            })
            return res.user.id
        except Exception as e:
            raise Exception(f"Erreur lors de la création de l'utilisateur Supabase: {str(e)}")

    def set_user_claims(self, uid: str, role: str):
        """
        Définit les rôles via les user_metadata dans Supabase.
        Ces métadonnées sont incluses dans le JWT.
        """
        if not self.client:
            raise Exception("Supabase non configuré.")
            
        try:
            self.client.auth.admin.update_user_by_id(
                uid,
                {"user_metadata": {"role": role}}
            )
        except Exception as e:
            raise Exception(f"Erreur lors de la définition des rôles Supabase: {str(e)}")

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Récupère un utilisateur par son email (via Admin API).
        Note: Supabase ne permet pas directement get_user_by_email simplement, 
        on doit lister les utilisateurs ou utiliser une astuce.
        """
        if not self.client:
            return None
            
        try:
            # On liste les utilisateurs et on filtre (Attention : limitation de pagination possible)
            users = self.client.auth.admin.list_users()
            for user in users:
                if user.email == email:
                    return {
                        'uid': user.id,
                        'email': user.email,
                        'display_name': user.user_metadata.get('display_name'),
                        'claims': user.user_metadata
                    }
            return None
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de l'utilisateur Supabase: {str(e)}")

    def update_user_password(self, uid: str, new_password: str):
        """Met à jour le mot de passe via Admin API."""
        if not self.client:
            raise Exception("Supabase non configuré.")
            
        try:
            self.client.auth.admin.update_user_by_id(uid, {"password": new_password})
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour du mot de passe Supabase: {str(e)}")

    def delete_user(self, uid: str):
        """Supprime un utilisateur Supabase via Admin API."""
        if not self.client:
            raise Exception("Supabase non configuré.")
            
        try:
            self.client.auth.admin.delete_user(uid)
        except Exception as e:
            raise Exception(f"Erreur lors de la suppression de l'utilisateur Supabase: {str(e)}")
