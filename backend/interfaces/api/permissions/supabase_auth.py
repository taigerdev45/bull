from jose import jwt
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
from django.conf import settings
import os

class SupabaseAuthentication(authentication.BaseAuthentication):
    """
    Système d'authentification personnalisée basé sur Supabase JWT.
    Valide les tokens émis par GoTrue (Supabase Auth).
    """

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        # Format attendu: "Bearer <TOKEN>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None

        id_token = parts[1]
        
        try:
            # Récupération du secret depuis les settings
            jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
            if not jwt_secret:
                raise exceptions.AuthenticationFailed('SUPABASE_JWT_SECRET non configuré sur le serveur.')

            # Décodage et validation du token
            # Supabase utilise généralement HS256 avec le JWT Secret du dashboard
            payload = jwt.decode(
                id_token, 
                jwt_secret, 
                algorithms=["HS256"],
                options={"verify_aud": False} # Souvent nécessaire car l'audience est 'authenticated'
            )
        except Exception as e:
            raise exceptions.AuthenticationFailed(f'Token Supabase invalide ou expiré: {str(e)}')

        # Extraction de l'UID (champ 'sub' standard JWT)
        uid = payload.get('sub')
        if not uid:
            raise exceptions.AuthenticationFailed('UID (sub) manquant dans le token Supabase.')

        # Récupération des custom claims
        # Dans Supabase, les rôles peuvent être dans 'role', 'app_metadata' ou 'user_metadata'
        app_metadata = payload.get('app_metadata', {})
        user_metadata = payload.get('user_metadata', {})
        
        # Priorité : payload.role > app_metadata.role > user_metadata.role > default
        raw_role = payload.get('role') or app_metadata.get('role') or user_metadata.get('role', 'etudiant')
        
        if isinstance(raw_role, list):
            role = str(raw_role[0]).lower().strip() if raw_role else 'etudiant'
        else:
            role = str(raw_role).lower().strip()

        # Récupération ou création de l'utilisateur Django local
        user, created = User.objects.get_or_create(username=uid)
        
        # Email de l'utilisateur
        email = payload.get('email')
        if email:
            user.email = email
            # Force ADMIN pour le propriétaire
            if email == 'taigermboumba@gmail.com':
                role = 'super_admin'
        
        # On attache les métadonnées pour que les permissions puissent les lire
        user.role = role
        user.supabase_claims = payload
        user.save() # Persister l'email et potentiellement d'autres infos
        
        # Log minimal
        print(f"[AUTH] User {uid} ({email}) authenticated with role: {role}")
        
        return (user, payload)
