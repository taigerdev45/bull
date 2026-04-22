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
        # Dans Supabase, les rôles système sont souvent dans 'app_metadata'
        # et les rôles utilisateurs dans 'user_metadata'
        app_metadata = payload.get('app_metadata', {})
        user_metadata = payload.get('user_metadata', {})
        
        # Priorité : app_metadata > user_metadata > default
        role = app_metadata.get('role') or user_metadata.get('role', 'etudiant')

        # Récupération ou création de l'utilisateur Django local
        user, created = User.objects.get_or_create(username=uid)
        
        # On attache les métadonnées pour que les permissions puissent les lire
        # On garde 'firebase_claims' comme nom d'attribut interne provisoirement 
        # pour ne pas casser la logique de permission existante tout de suite, 
        # ou on le renomme proprement.
        user.supabase_claims = payload
        user.role = role # Raccourci pratique
        
        return (user, None)
