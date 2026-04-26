import os
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions


def _extract_role(user_data: dict) -> str:
    """
    Extrait le rôle depuis les métadonnées Supabase.
    Priorité: app_metadata.role > user_metadata.role > 'etudiant' (défaut)
    Le claim 'role' racine du JWT est toujours 'authenticated' pour Supabase ---
    on ne l'utilise JAMAIS.
    """
    app_metadata = user_data.get('app_metadata') or {}
    user_metadata = user_data.get('user_metadata') or {}

    role = (
        app_metadata.get('role')
        or user_metadata.get('role')
        or 'etudiant'
    )

    if isinstance(role, list):
        role = role[0] if role else 'etudiant'

    return str(role).lower().strip()


class SupabaseAuthentication(authentication.BaseAuthentication):
    """
    Authentification Supabase via l'API Admin (get_user).
    Valide le token ACCESS de Supabase en appelant l'endpoint GoTrue /auth/v1/user,
    ce qui ne dépend pas du SUPABASE_JWT_SECRET local.
    Fallback: décodage JWT local si SUPABASE_JWT_SECRET est disponible.
    """

    def _get_user_from_supabase_api(self, token: str) -> dict | None:
        """Valide le token en appelant l'API Supabase GoTrue."""
        try:
            from supabase import create_client
            supabase_url = os.getenv("SUPABASE_URL", "")
            # On peut utiliser la service_role_key pour créer le client admin
            # puis valider le token utilisateur via get_user(token)
            service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

            if not supabase_url or not service_key:
                print("[AUTH] SUPABASE_URL ou SUPABASE_SERVICE_ROLE_KEY non configuré.")
                return None

            client = create_client(supabase_url, service_key)
            # get_user(jwt) valide le token et retourne l'utilisateur correspondant
            res = client.auth.get_user(token)
            if res and res.user:
                user = res.user
                return {
                    'sub': user.id,
                    'email': user.email,
                    'app_metadata': user.app_metadata or {},
                    'user_metadata': user.user_metadata or {},
                }
        except Exception as e:
            print(f"[AUTH] Supabase API validation failed: {e}")
        return None

    def _get_user_from_jwt_decode(self, token: str) -> dict | None:
        """Tente de décoder le JWT localement (fallback)."""
        try:
            from jose import jwt as jose_jwt
            jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
            if not jwt_secret:
                return None
            payload = jose_jwt.decode(
                token,
                jwt_secret,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
            return {
                'sub': payload.get('sub'),
                'email': payload.get('email'),
                'app_metadata': payload.get('app_metadata') or {},
                'user_metadata': payload.get('user_metadata') or {},
            }
        except Exception as e:
            print(f"[AUTH] JWT local decode failed: {e}")
        return None

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return None

        token = parts[1]

        # Stratégie 1 : Validation via API Supabase (méthode préférée)
        user_data = self._get_user_from_supabase_api(token)

        # Stratégie 2 : Décodage JWT local (fallback)
        if user_data is None:
            user_data = self._get_user_from_jwt_decode(token)

        if user_data is None:
            print(f"[AUTH FAILED] Token rejected by all methods.")
            return None

        uid = user_data.get('sub')
        if not uid:
            raise exceptions.AuthenticationFailed('UID (sub) manquant dans le token.')

        email = user_data.get('email', '')
        role = _extract_role(user_data)

        # Bypass propriétaire
        if email == 'taigermboumba@gmail.com':
            role = 'super_admin'

        # Récupération ou création de l'utilisateur Django local
        user, _ = User.objects.get_or_create(username=uid)
        if email:
            user.email = email
        if email == 'taigermboumba@gmail.com':
            user.is_superuser = True
            user.is_staff = True

        user.role = role
        user.supabase_claims = user_data
        user.firebase_claims = user_data
        user.save()

        print(f"[AUTH SUCCESS] UID: {uid} | Email: {email} | Role: {role}")
        print(f"[AUTH CLAIMS] App: {user_data.get('app_metadata')} | User: {user_data.get('user_metadata')}")

        return (user, user_data)
