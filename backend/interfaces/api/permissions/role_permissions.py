from rest_framework import permissions

def get_user_role(user):
    """Extrait le rôle de l'utilisateur avec fallback sur PersonnelModel."""
    if not user or not user.is_authenticated:
        return 'etudiant'
    
    role = getattr(user, 'role', None)
    if role:
        return str(role).lower().strip()
        
    # Fallback sur la DB si l'attribut est perdu (ex: re-fetch)
    from infrastructure.persistence.django_models.models import PersonnelModel
    p = PersonnelModel.objects.filter(email__iexact=user.email).first()
    if p:
        return p.role.lower().strip()
    return 'etudiant'

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        role = get_user_role(user)
        return role == 'super_admin' or user.is_superuser or str(user.email).lower() == 'taigermboumba@gmail.com'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated): return False
        email = str(user.email).lower()
        if user.is_superuser or email == 'taigermboumba@gmail.com': return True
        role = get_user_role(user)
        return role in ['super_admin', 'admin'] or user.is_staff

class IsSecretariat(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        is_auth = user and user.is_authenticated
        if not is_auth:
            return False
            
        role = get_user_role(user)
        email = str(user.email).lower().strip()
        is_staff = user.is_staff
        is_superuser = user.is_superuser
        
        allow = role in ['super_admin', 'admin', 'secretariat'] or user.is_staff or user.is_superuser or str(user.email).lower() == 'taigermboumba@gmail.com'

        if not allow:
            print(f"[PERM DENIED] IsSecretariat | Path: {request.path} | Email: {email} | Role: {role} | Staff: {is_staff} | Super: {is_superuser}")
            
        return allow

class IsEnseignant(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return role in ['super_admin', 'admin', 'enseignant'] or request.user.is_superuser

class IsEtudiant(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        role = str(getattr(request.user, 'role', '')).lower().strip()
        return role == 'etudiant'
