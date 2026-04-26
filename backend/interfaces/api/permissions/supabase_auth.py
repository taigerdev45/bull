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
            # Au lieu de bloquer avec une exception, on retourne None
            # Cela permet aux vues avec 'AllowAny' de fonctionner même si le token est expiré.
            # Les vues protégées bloqueront de toute façon plus tard.
            print(f"[AUTH] Token validation failed: {str(e)}")
            return None

        # Extraction de l'UID (champ 'sub' standard JWT)
        uid = payload.get('sub')
        if not uid:
            raise exceptions.AuthenticationFailed('UID (sub) manquant dans le token Supabase.')

        # Récupération des custom claims
        # Dans Supabase, les rôles peuvent être dans 'role', 'app_metadata' ou 'user_metadata'
        app_metadata = payload.get('app_metadata', {})
        user_metadata = payload.get('user_metadata', {})
        
        # Priorité : app_metadata.role > user_metadata.role > payload.role > default
        # Note: Dans Supabase, 'role' est souvent simplement 'authenticated' par défaut, 
        # on ne doit l'utiliser que si rien d'autre n'est défini ou si c'est une valeur spécifique.
        
        role = 'etudiant' # Défaut
        
        if app_metadata.get('role'):
            role = app_metadata.get('role')
        elif user_metadata.get('role'):
            role = user_metadata.get('role')
        elif payload.get('role') and payload.get('role') != 'authenticated':
            role = payload.get('role')
        
        if isinstance(role, list):
            role = str(role[0]).lower().strip() if role else 'etudiant'
        else:
            role = str(role).lower().strip()

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
        user.firebase_claims = payload # Compatibilité avec l'ancien code
        
        # Bypass ultime pour le propriétaire
        if user.email == 'taigermboumba@gmail.com':
            user.is_superuser = True
            user.is_staff = True
            
        user.save() # Persister l'email et potentiellement d'autres infos
        
        # Log détaillé (visible sur Render)
        print(f"[AUTH SUCCESS] UID: {uid} | Email: {user.email} | Detected Role: {role}")
        print(f"[AUTH CLAIMS] App Meta: {app_metadata} | User Meta: {user_metadata} | Global Role: {payload.get('role')}")
        
        return (user, payload)
