from django.db.models import Q
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions
import os


def _extract_role(user_data: dict) -> str:
    """
    Extrait le role depuis les metadonnees Supabase.
    Priorite: app_metadata.role > user_metadata.role > 'etudiant' (defaut)
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
    """

    def _get_user_from_supabase_api(self, token: str) -> dict | None:
        """Valide le token en appelant l'API Supabase GoTrue."""
        try:
            from supabase import create_client
            supabase_url = os.getenv("SUPABASE_URL", "")
            service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

            if not supabase_url or not service_key:
                return None

            client = create_client(supabase_url, service_key)
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
        """Tente de decoder le JWT localement (fallback)."""
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

        # Strategie 1 : Validation via API Supabase
        user_data = self._get_user_from_supabase_api(token)

        # Strategie 2 : Fallback JWT local
        if user_data is None:
            user_data = self._get_user_from_jwt_decode(token)

        if user_data is None:
            return None

        uid = user_data.get('sub')
        if not uid:
            raise exceptions.AuthenticationFailed('UID (sub) manquant.')

        email = str(user_data.get('email', '')).lower().strip()
        role = _extract_role(user_data)
        
        # Bypass proprietaire
        is_owner = email == 'taigermboumba@gmail.com'

        # --- RECONCILIATION ET FALLBACK ---
        if not is_owner:
            from infrastructure.persistence.django_models.models import PersonnelModel, EnseignantModel, EtudiantModel
            
            # Recherche croisee UID ou Email (insensible a la casse)
            personnel = PersonnelModel.objects.filter(Q(user_id=uid) | Q(email__iexact=email)).first()
            if personnel:
                role = personnel.role
                if personnel.user_id != uid:
                    personnel.user_id = uid
                    personnel.save()
            else:
                enseignant = EnseignantModel.objects.filter(Q(user_id=uid) | Q(email__iexact=email)).first()
                if enseignant:
                    role = 'enseignant'
                    if enseignant.user_id != uid:
                        enseignant.user_id = uid
                        enseignant.save()
                else:
                    etudiant = EtudiantModel.objects.filter(Q(user_id=uid) | Q(email__iexact=email)).first()
                    if etudiant:
                        role = 'etudiant'
                        if etudiant.user_id != uid:
                            etudiant.user_id = uid
                            etudiant.save()
        else:
            role = 'super_admin'
                
        # Synchronisation Utilisateur Django
        user, created = User.objects.get_or_create(username=uid)
        user.email = email
        user.is_active = True
        
        # Attribution des droits staff/superuser
        is_staff_role = role in ['super_admin', 'admin', 'secretariat', 'staff']
        user.is_staff = is_staff_role
        
        if role == 'super_admin' or is_owner:
            user.is_superuser = True
            user.is_staff = True

        # Sauvegarde obligatoire pour persister is_staff
        user.save()

        # Injection des meta-donnees
        user.role = role
        user.uid = uid
        user.supabase_claims = user_data
        user.firebase_claims = user_data

        print(f"[AUTH SUCCESS] UID: {uid} | Email: {email} | Role: {role} | Staff: {user.is_staff}")

        return (user, user_data)
